
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from classes.parsezeeklogs import ParseZeekLogs
from netaddr import IPNetwork, IPAddress
from utils import get_iocs, get_config, get_whitelist
from ipwhois import IPWhois
import subprocess as sp
import json
import pydig
import os


class ZeekEngine(object):

    def __init__(self, capture_directory):
        self.working_dir = capture_directory
        self.alerts = []
        self.conns = []
        self.ssl = []
        self.http = []
        self.dns = []
        self.files = []
        self.whitelist = []

        # Get analysis configuration
        self.heuristics_analysis = get_config(("analysis", "heuristics"))
        self.iocs_analysis = get_config(("analysis", "iocs"))
        self.whitelist_analysis = get_config(("analysis", "whitelist"))

    def fill_dns(self, dir):
        """
            Fill the DNS resolutions thanks to the dns.log.
            :return: nothing - all resolutions appended to self.dns.
        """
        if os.path.isfile(os.path.join(dir, "dns.log")):
            for record in ParseZeekLogs(os.path.join(dir, "dns.log"), output_format="json", safe_headers=False):
                if record is not None:
                    if record["qtype_name"] in ["A", "AAAA"]:
                        d = {"domain": record["query"],
                             "answers": record["answers"].split(",")}
                        if d not in self.dns:
                            self.dns.append(d)

    def netflow_check(self, dir):
        """
            Enrich and check the netflow from the conn.log against whitelist and IOCs.
            :return: nothing - all stuff appended to self.alerts
        """
        max_ports = get_config(("analysis", "max_ports"))
        http_default_port = get_config(("analysis", "http_default_port"))

        # Get the netflow from conn.log.
        if os.path.isfile(os.path.join(dir, "conn.log")):
            for record in ParseZeekLogs(os.path.join(dir, "conn.log"), output_format="json", safe_headers=False):
                if record is not None:
                    c = {"ip_dst": record["id.resp_h"],
                         "proto": record["proto"],
                         "port_dst": record["id.resp_p"],
                         "service": record["service"],
                         "alert_tiggered": False}
                    if c not in self.conns:
                        self.conns.append(c)

        # Let's add some dns resolutions.
        for c in self.conns:
            c["resolution"] = self.resolve(c["ip_dst"])

        # Order the conns list by the resolution field.
        self.conns = sorted(self.conns, key=lambda c: c["resolution"])

        # Check for whitelisted assets, if any, delete the record.
        if self.whitelist_analysis:

            wl_cidrs = [IPNetwork(cidr) for cidr in get_whitelist("cidr")]
            wl_hosts = get_whitelist("ip4addr") + get_whitelist("ip6addr")
            wl_domains = get_whitelist("domain")

            for i, c in enumerate(self.conns):
                if c["ip_dst"] in [ip for ip in wl_hosts]:
                    self.whitelist.append(self.conns[i])
                    self.conns[i] = False
                elif c["resolution"] in wl_domains:
                    self.whitelist.append(self.conns[i])
                    self.conns[i] = False
                elif True in [c["resolution"].endswith("." + dom) for dom in wl_domains]:
                    self.whitelist.append(self.conns[i])
                    self.conns[i] = False
                elif True in [IPAddress(c["ip_dst"]) in cidr for cidr in wl_cidrs]:
                    self.whitelist.append(self.conns[i])
                    self.conns[i] = False

            # Let's delete whitelisted connections.
            self.conns = list(filter(lambda c: c != False, self.conns))

        if self.heuristics_analysis:
            for c in self.conns:
                # Check for UDP / ICMP (strange from a smartphone.)
                if c["proto"] in ["UDP", "ICMP"]:
                    c["alert_tiggered"] = True
                    self.alerts.append({"title": "{} communication going outside the local network to {}.".format(c["proto"].upper(), c["resolution"]),
                                        "description": "The {} protocol is commonly used in internal networks. Please, verify if the host {} leveraged other alerts which may ".format(c["proto"].upper(), c["resolution"])
                                        + "indicates a possible malicious behavior.",
                                        "host": c["resolution"],
                                        "level": "Moderate",
                                        "id": "PROTO-01"})
                # Check for use of ports over 1024.
                if c["port_dst"] >= max_ports:
                    c["alert_tiggered"] = True
                    self.alerts.append({"title": "{} connection to {} to a port over or equal to {}.".format(c["proto"].upper(), c["resolution"], max_ports),
                                        "description": "{} connections have been seen to {} by using the port {}. The use of non-standard port can be sometimes associated to malicious activities. ".format(c["proto"].upper(), c["resolution"], c["port_dst"])
                                        + "We recommend to check if this host has a good reputation by looking on other alerts and search it on the internet.",
                                        "host": c["resolution"],
                                        "level": "Low",
                                        "id": "PROTO-02"})
                # Check for use of HTTP.
                if c["service"] == "http" and c["port_dst"] == http_default_port:
                    c["alert_tiggered"] = True
                    self.alerts.append({"title": "HTTP communications have been done to the host {}".format(c["resolution"]),
                                        "description": "Your device exchanged with the host {} by using HTTP, an unencrypted protocol. ".format(c["resolution"])
                                        + "Even if this behavior is not malicious by itself, it is unusual to see HTTP communications issued from smartphone applications "
                                        + "running in the background. Please check the host reputation by searching it on the internet.",
                                        "host": c["resolution"],
                                        "level": "Low",
                                        "id": "PROTO-03"})

                # Check for use of HTTP on a non standard port.
                if c["service"] == "http" and c["port_dst"] != http_default_port:
                    c["alert_tiggered"] = True
                    self.alerts.append({"title": "HTTP communications have been seen to the host {} on a non standard port ({}).".format(c["resolution"], c["port_dst"]),
                                        "description": "Your device exchanged with the host {} by using HTTP, an unencrypted protocol on the port {}. ".format(c["resolution"], c["port_dst"])
                                        + "This behavior is quite unusual. Please check the host reputation by searching it on the internet.",
                                        "host": c["resolution"],
                                        "level": "Moderate",
                                        "id": "PROTO-04"})
                # Check for non-resolved IP address.
                if c["service"] == c["resolution"]:
                    c["alert_tiggered"] = True
                    self.alerts.append({"title": "The server {} hasn't been resolved by any DNS query during the session".format(c["ip_dst"]),
                                        "description": "It means that the server {} is likely not resolved by any domain name or the resolution has already been cached by ".format(c["ip_dst"])
                                        + "the device. If the host appears in other alerts, please check it.",
                                        "host": c["ip_dst"],
                                        "level": "Low",
                                        "id": "PROTO-05"})

        if self.iocs_analysis:

            bl_cidrs = [[IPNetwork(cidr[0]), cidr[1]]
                        for cidr in get_iocs("cidr")]
            bl_hosts = get_iocs("ip4addr") + get_iocs("ip6addr")
            bl_domains = get_iocs("domain")
            bl_freedns = get_iocs("freedns")
            bl_nameservers = get_iocs("ns")
            bl_tlds = get_iocs("tld")

            for c in self.conns:
                # Check for blacklisted IP address.
                for host in bl_hosts:
                    if c["ip_dst"] == host[0]:
                        c["alert_tiggered"] = True
                        self.alerts.append({"title": "A connection has been made to {} ({}) which is tagged as {}.".format(c["resolution"], c["ip_dst"], host[1].upper()),
                                            "description": "The host {} has been explicitly blacklisted for malicious activities. Your device is likely compromised ".format(c["ip_dst"])
                                            + "and needs to be investigated more deeply by IT security professionals.",

                                            "host": c["resolution"],
                                            "level": "High",
                                            "id": "IOC-01"})
                        break
                # Check for blacklisted CIDR.
                for cidr in bl_cidrs:
                    if IPAddress(c["ip_dst"]) in cidr[0]:
                        c["alert_tiggered"] = True
                        self.alerts.append({"title": "Communication to {} under the CIDR {} which is tagged as {}.".format(c["resolution"], cidr[0], cidr[1].upper()),
                                            "description": "The server {} is hosted under a network which is known to host malicious activities. Even if this behavior is not malicious by itself, ".format(c["resolution"])
                                            + "you need to check if other alerts are also mentioning this host. If you have some doubts, please "
                                            + "search this host on the internet to see if its legit or not.",
                                            "host": c["resolution"],
                                            "level": "Moderate",
                                            "id": "IOC-02"})
                # Check for blacklisted domain.
                for domain in bl_domains:
                    if c["resolution"].endswith(domain[0]):
                        if domain[1] != "tracker":
                            c["alert_tiggered"] = True
                            self.alerts.append({"title": "A DNS request have been done to {} which is tagged as {}.".format(c["resolution"], domain[1].upper()),
                                                "description": "The domain name {} seen in the capture has been explicitly tagged as malicious. This indicates that ".format(c["resolution"])
                                                + "your device is likely compromised and needs to be investigated deeply.",
                                                "host": c["resolution"],
                                                "level": "High",
                                                "id": "IOC-03"})
                        else:
                            c["alert_tiggered"] = True
                            self.alerts.append({"title": "A DNS request have been done to {} which is tagged as {}.".format(c["resolution"], domain[1].upper()),
                                                "description": "The domain name {} seen in the capture has been explicitly tagged as a Tracker. This ".format(c["resolution"])
                                                + "indicates that one of the active apps is geo-tracking your moves.",
                                                "host": c["resolution"],
                                                "level": "Moderate",
                                                "id": "IOC-03"})
                # Check for blacklisted FreeDNS.
                for domain in bl_freedns:
                    if c["resolution"].endswith("." + domain[0]):
                        c["alert_tiggered"] = True
                        self.alerts.append({"title": "A DNS request have been done to the domain {} which is a Free DNS.".format(c["resolution"]),
                                            "description": "The domain name {} is using a Free DNS service. This kind of service is commonly used by cybercriminals ".format(c["resolution"])
                                            + "or state-sponsored threat actors during their operations. It is very suspicious that an application running in background use this kind of service, please investigate.",
                                            "host": c["resolution"],
                                            "level": "Moderate",
                                            "id": "IOC-04"})

                # Check for suspect tlds.
                for tld in bl_tlds:
                    if c["resolution"].endswith(tld[0]):
                        c["alert_tiggered"] = True
                        self.alerts.append({"title": "A DNS request have been done to the domain {} which contains a suspect TLD.".format(c["resolution"]),
                                            "description": "The domain name {} is using a suspect Top Level Domain ({}). Even not malicious, this non-generic TLD is used regularly by cybercrime ".format(c["resolution"], tld[0])
                                            + "or state-sponsored operations. Please check this domain by searching it on an internet search engine. If other alerts are related to this "
                                            + "host, please consider it as very suspicious.",
                                            "host": c["resolution"],
                                            "level": "Low",
                                            "id": "IOC-05"})

                # Check for use of suspect nameservers.
                try:
                    name_servers = pydig.query(c["resolution"], "NS")
                except:
                    name_servers = []

                if len(name_servers):
                    for ns in bl_nameservers:
                        if name_servers[0].endswith(".{}.".format(ns[0])):
                            c["alert_tiggered"] = True
                            self.alerts.append({"title": "The domain {} is using a suspect nameserver ({}).".format(c["resolution"], name_servers[0]),
                                                "description": "The domain name {} is using a nameserver that has been explicitly tagged to be associated to malicious activities. ".format(c["resolution"])
                                                + "Many cybercriminals and state-sponsored threat actors are using this kind of registrars because they allow cryptocurrencies and anonymous payments. It"
                                                + " is adviced to investigate on this domain and the associated running application by doing a forensic analysis of the phone.",
                                                "host": c["resolution"],
                                                "level": "Moderate",
                                                "id": "IOC-06"})

    def files_check(self, dir):
        """
            Check on the files.log:
                * Check certificates sha1
                * [todo] Check possible binary data or APKs?
            :return: nothing - all stuff appended to self.alerts
        """

        if not self.iocs_analysis:
            return

        bl_certs = get_iocs("sha1cert")

        if os.path.isfile(os.path.join(dir, "files.log")):
            for record in ParseZeekLogs(os.path.join(dir, "files.log"), output_format="json", safe_headers=False):
                if record is not None:
                    f = {"filename": record["filename"],
                         "ip_src": record["tx_hosts"],
                         "ip_dst": record["rx_hosts"],
                         "mime_type": record["mime_type"],
                         "sha1": record["sha1"]}
                    if f not in self.files:
                        self.files.append(f)

        for f in self.files:
            if f["mime_type"] == "application/x-x509-ca-cert":
                for cert in bl_certs:  # Check for blacklisted certificate.
                    if f["sha1"] == cert[0]:
                        host = self.resolve(f["ip_dst"])
                        c["alert_tiggered"] = True
                        self.alerts.append({"title": "A certificate associated to {} activities have been found in the communication to {}.".format(cert[1].upper(), host),
                                            "description": "The certificate ({}) associated to {} has been explicitly tagged as malicious. This indicates that ".format(f["sha1"], host)
                                            + "your device is likely compromised and need a forensic analysis.",
                                            "host": host,
                                            "level": "High",
                                            "id": "IOC-07"})

    def ssl_check(self, dir):
        """
            Check on the ssl.log:
                * SSL connections which doesn't use the 443.
                * "Free" certificate issuer (taken from the config).
                * Self-signed certificates.
            :return: nothing - all stuff appended to self.alerts
        """
        ssl_default_ports = get_config(("analysis", "ssl_default_ports"))
        free_issuers = get_config(("analysis", "free_issuers"))

        if os.path.isfile(os.path.join(dir, "ssl.log")):
            for record in ParseZeekLogs(os.path.join(dir, "ssl.log"), output_format="json", safe_headers=False):
                if record is not None:
                    c = {"host": record['id.resp_h'],
                         "port": record['id.resp_p'],
                         "issuer": record["issuer"],
                         "validation_status": record["validation_status"]}
                    if c not in self.ssl:
                        self.ssl.append(c)

        if self.heuristics_analysis:
            for cert in self.ssl:
                host = self.resolve(cert["host"])

                # If the associated host has not whitelisted, check the cert.
                for c in self.conns:
                    if host in c["resolution"]:
                        # Check for non generic SSL port.
                        if cert["port"] not in ssl_default_ports:
                            c["alert_tiggered"] = True
                            self.alerts.append({"title": "SSL connection done on a non standard port ({}) to {}".format(cert["port"], host),
                                                "description": "It is not common to see SSL connections issued from smartphones using non-standard ports. Even this can be totally legit,"
                                                + " we recommend to check the reputation of {}, by looking at its WHOIS record, the associated autonomus system, its creation date, and ".format(host)
                                                + " by searching it the internet.",
                                                "host": host,
                                                "level": "Moderate",
                                                "id": "SSL-01"})
                        # Check Free SSL certificates.
                        if cert["issuer"] in free_issuers:
                            c["alert_tiggered"] = True
                            self.alerts.append({"title": "An SSL connection to {} is using a free certificate.".format(host),
                                                "description": "Free certificates — such as Let's Encrypt — are wildly used by command and control servers associated to "
                                                + "malicious implants or phishing web pages. We recommend to check the host associated to this certificate, "
                                                + "by looking at the domain name, its creation date, or by checking its reputation on the internet.",
                                                "host": host,
                                                "level": "Moderate",
                                                "id": "SSL-02"})
                        # Check for self-signed certificates.
                        if cert["validation_status"] == "self signed certificate in certificate chain":
                            c["alert_tiggered"] = True
                            self.alerts.append({"title": "The certificate associated to {} is self-signed.".format(host),
                                                "description": "The use of self-signed certificates is a common thing for attacker infrastructure. We recommend to check the host {} ".format(host)
                                                + "which is associated to this certificate, by looking at the domain name (if any), its WHOIS record, its creation date, and "
                                                + " by checking its reputation on the internet.",
                                                "host": host,
                                                "level": "Moderate",
                                                "id": "SSL-03"})

    def alerts_check(self):
        """
            Leverage an advice to the user based on the trigered hosts
            :return: nothing - all generated alerts appended to self.alerts
        """
        hosts = {}

        for alert in [dict(t) for t in {tuple(d.items()) for d in self.alerts}]:
            if alert["host"] not in hosts:
                hosts[alert["host"]] = 1
            else:
                hosts[alert["host"]] += 1

        for host, nb in hosts.items():
            if nb >= get_config(("analysis", "max_alerts")):
                self.alerts.append({"title": "Check alerts for {}".format(host),
                                    "description": "Please, check the reputation of the host {}, this one seems to be malicious as it leveraged {} alerts during the session.".format(host, nb),
                                    "host": host,
                                    "level": "High",
                                    "id": "ADV-01"})

    def resolve(self, ip_addr):
        """
            A simple method to retreive DNS names from IP addresses
            in order to replace them in alerts.

            :return: String - DNS record or IP Address.
        """
        for record in self.dns:
            if ip_addr in record["answers"]:
                return record["domain"]
        return ip_addr

    def start_zeek(self):
        """
            Start zeek and check the logs.
        """
        sp.Popen("cd {} && /opt/zeek/bin/zeek -Cr capture.pcap protocols/ssl/validate-certs".format(
            self.working_dir), shell=True).wait()
        sp.Popen("cd {} && mv *.log assets/".format(self.working_dir),
                 shell=True).wait()

        self.fill_dns(self.working_dir + "/assets/")
        self.netflow_check(self.working_dir + "/assets/")
        self.ssl_check(self.working_dir + "/assets/")
        self.files_check(self.working_dir + "/assets/")
        self.alerts_check()

    def retrieve_alerts(self):
        """
            Retrieve alerts.
            :return: list - a list of alerts wihout duplicates.
        """
        return [dict(t) for t in {tuple(d.items()) for d in self.alerts}]

    def retrieve_whitelist(self):
        """
            Retrieve whitelisted elements.
            :return: list - a list of whitelisted elements wihout duplicates.
        """
        return [dict(t) for t in {tuple(d.items()) for d in self.whitelist}]

    def retrieve_conns(self):
        """
            Retrieve not whitelisted elements.
            :return: list - a list of non-whitelisted elements wihout duplicates.
        """
        return self.conns
