# TinyCheck

### Description

TinyCheck allows you to easily capture network communications from a smartphone or any device which can be associated to a Wi-Fi access point in order to quickly analyze them. This can be used to check if any suspect or malicious communication is outgoing from a smartphone, by using heuristics or specific Indicators of Compromise (IoCs).

The idea of TinyCheck emerged in a meeting about stalkerware with a [French women's shelter](https://www.centre-hubertine-auclert.fr). During this meeting we talked about how to easily detect [stalkerware](https://stopstalkerware.org/) without installing very technical apps nor doing forensic analysis on the victim's smartphone. The initial concept was to develop a tiny kiosk device based on Raspberry Pi which can be used by non-tech people to test their smartphones against malicious communications issued by stalkerware or any spyware.

Of course, TinyCheck can also be used to spot any malicious communications from cybercrime to state-sponsored implants. It allows the end-user to push his own extended Indicators of Compromise via a backend in order to detect some ghosts over the wire.

<p align="center"> *If you need more documentation on how to install it, use it and the internals, don't hesitate to take a look at the [TinyCheck Wiki](https://github.com/KasperskyLab/TinyCheck/wiki).* </p>

*If you have any question about the projet. Want to contribute or just send your feedbacks, don't hesitate to contact us at tinycheck[@]kaspersky[.]com.*

![Architecture](/assets/network-home.png)

### Use cases

TinyCheck can be used in several ways by individuals and entities:

- Over a network - TinyCheck is installed on a network and can be accessed from a workstation via a browser.
- In kiosk mode - TinyCheck can be used as a kiosk to allow visitors to test their own devices.
- Fully standalone - By using a powerbank, two Wi-Fi interfaces or a 4G dongle and a small touch screen [like in this video](https://twitter.com/felixaime/status/1331535790392946689), you can tap any device anywhere.

### Installation

Please check the few steps in the [Wiki's Installation Page](https://github.com/KasperskyLab/TinyCheck/wiki/TinyCheck-installation). 

### Meet the frontend

The frontend - which can be accessed from `http://tinycheck.local` or `http://127.0.0.1` if you are running it locally - is a kind of tunnel which help the user throughout the process of network capture and reporting. It allows the user to setup a Wi-Fi connection to an existing Wi-Fi network, create an ephemeral Wi-Fi network, capture the communications and show a report to the user... in less than one minute, 5 clicks and without any technical knowledge. 

![Frontend](/assets/frontend.png)

### Meet the backend

Once installed, you can connect yourself to the TinyCheck backend by browsing the URL `https://tinycheck.local` or  `http://127.0.0.1` if you are running it locally and accepting the SSL self-signed certificate. 

![Backend](/assets/backend.png)

The backend allows you to edit the configuration of TinyCheck, add extended IOCs and whitelisted elements in order to prevent false positives. Several IOCs are already provided such as few suricata rules, FreeDNS, Name servers, CIDRs known to host malicious servers and so on. In term of extended IOCs, this first version of TinyCheck includes:

- Suricata rules
- CIDRs
- Domains & FQDNs (named generically "Domains")
- IPv4 / IPv6 Addresses
- Certificates sha1
- Nameservers
- FreeDNS
- Fancy TLDs (eg. xyz, .top etc.)

### Meet the analysis engine

The analysis engine is pretty straightforward. For this first version, the network communications are not analyzed in real time during the capture. The engine executes Zeek and Suricata against the previously saved network capture. [Zeek](https://zeek.org/) is a well-known network dissector which stores in several logs the captured session. 

Once saved, these logs are analysed to find extended IOCs (listed above) or to match heuristics rules (which can be deactivated through the backend). The heuristics rules are hardcoded in `zeekengine.py`, and they are listed below. As only one device is analyzed at a time, there is a low probability to see heuristic alerts leveraged.

- UDP/ICMP going outside the local network
- UDP/TCP connection with a destination port >1024
- Remote host not resolved by DNS during the session
- Use of self-signed certificate by the remote host
- SSL connection done on a non standard port
- Use of specific SSL certificates issuers by the remote host (such as Let's Encrypt)
- HTTP requests done during the session
- HTTP requests done on a non standard port
- ...

On the [Suricata](https://suricata-ids.org/) part, the network capture is analysed against suricata rules saved as IOCs. Few rules are dynamics such as:

- Device name exfiltred in clear-text;
- Access point SSID exfiltred in clear-text;

### Watchers concept

In order to keep IOCs and whitelist updated constantly, TinyCheck integrates something called "watchers". It is a very simple service with few lines of Python which grabs new formated IOCs or whitelist elements from public URLs. As of today, TinyCheck integrates two urls, one for the whitelist and one for the IOCs (The formated files are present in the assets folder). 

If you have seen something very suspicious and/or needs to be investigated/integrated in one of these two lists, don't hesitate to ping us. You can also do you own watcher. Remember, sharing is caring. 

### Questions & Answers

**Your project seem very cool, does it send data to Kaspersky or any telemetry server?**<br /><br />
No, at all. You can look to the sources, the only data sent by TinyCheck is an HTTP GET request to a website that you can specify in the config, as well as the watchers URLs. Kaspersky don't - and will not - receive any telemetry from your TinyCheck device.<br /><br />
**Can you list some hardware which can be used with this project (touch screen, wifi dongle etc.)?**<br /><br />
Unfortunately, we prefer to not promote any hardware/constructor/website on this page. Do not hesitate to contact us if you want specific references. <br /><br />
**I'm not very confortable with the concept of "watchers" as the IOCs downloaded are public. Do you plan to develop a server to centralize AMBER/RED IOCs?**<br /><br />
Yes, if the demand is felt by NGOs (contact us!). Is it possible to develop this kind of thing, allowing you to centralize your IOCs and managing your fleet of TinyCheck instances on a server that you host. The server can also embed better detection rules thanks to the telemetry that it will receive from devices.<br />

### Possible updates for next releases

- More OpSec (TOR integration, Local IP randomization etc.)
- Possibility to add watchers from the backend interface.
- Centralized server for IOC/whitelist management (aka. Remote Analysis).
- Better frontend GUI/JS (use of websockets / better animations).
- Encryption of ZIPed reports.

### Contact

If you have any question about the projet. Want to contribute or just send your feedbacks/success stories, don't hesitate to contact us at tinycheck[@]kaspersky[.]com. 

### Special thanks

**Guys who provided some IOCs**
- [Cian Heasley](https://twitter.com/nscrutables) for his android stalkerwares IOC repo, available here: https://github.com/diskurse/android-stalkerware
- [Te-k](https://twitter.com/tenacioustek) for his stalkerwares awesome IOCs repo, available here: https://github.com/Te-k/stalkerware-indicators
- [Emilien](https://twitter.com/__Emilien__) for his Stratum rules, available here: https://github.com/kwouffe/cryptonote-hunt
- [Costin Raiu](https://twitter.com/craiu) for his geo-tracker domains, available here: https://github.com/craiu/mobiletrackers/blob/master/list.txt

**Code review**
- Dan Demeter [@_xdanx](https://twitter.com/_xdanx)
- Maxime Granier
- Florian Pires [@Florian_Pires](https://twitter.com/Florian_Pires)
- Ivan Kwiatkowski [@JusticeRage](https://twitter.com/JusticeRage)

**Others**
- GReAT colleagues.
- Tatyana, Kristina, Christina and Arnaud from Kaspersky (Support and IOCs)
- Zeek and Suricata awesome maintainers.
- virtual-keyboard.js.org & loading.io guys.
- Yan Zhu for his awesome Spectre CSS lib (https://picturepan2.github.io/spectre/)
