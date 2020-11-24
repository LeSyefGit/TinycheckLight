<template>
    <div class="backend-content" id="content">
        <div class="column col-6 col-xs-12">
            <h3 class="s-title">Network configuration</h3>
            <h5 class="s-subtitle">Interfaces configuration</h5>
            <img src="@/assets/network.png" id="network-thumbnail" />
            <div class="container interfaces-container">
                <div class="columns">
                    <div class="column col-6">
                        <span class="interface-label">First interface</span>
                        <div class="form-group">
                            <div class="btn-group btn-group-block">
                                <button class="btn btn-sm btn-iface" @click="change_interface('in', iface)" :class="iface == config.network.in ? 'active' : ''" v-for="iface in config.interfaces" :key="iface">{{ iface.toUpperCase() }}</button>
                            </div>
                        </div>
                    </div>
                    <div class="column col-6">
                        <span class="interface-label">Second interface</span>
                        <div class="form-group">
                            <div class="btn-group btn-group-block">
                                <button class="btn btn-sm btn-iface" @click="change_interface('out', iface)" :class="iface == config.network.out ? 'active' : ''" v-for="iface in config.interfaces" :key="iface">{{ iface.toUpperCase() }}</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <h5 class="s-subtitle">Edit SSIDs names</h5>
            <div class="form-group">
                <table class="table table-striped table-hover">
                    <tbody>
                        <tr v-for="ssid in config.network.ssids" :key="ssid">
                            <td>{{ ssid }}</td>
                            <td><button class="btn btn-sm" v-on:click="delete_ssid(ssid)">Delete</button></td>
                        </tr>
                        <tr>
                            <td><input class="form-input" v-model="ssid" type="text" placeholder="SSID name"></td>
                            <td><button class="btn btn-sm" @click="add_ssid()">Add</button></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'manageinterface',
    data() {
        return {
            config: {},
            ssid: ""
        }
    },
    props: {},
    methods: {
        async get_jwt() {
            await axios.get(`/api/get-token`, { timeout: 10000 })
                .then(response => {
                    if (response.data.token) {
                        this.jwt = response.data.token
                    }
                })
                .catch(err => (console.log(err)))
        },
        load_config: function() {
            axios.get(`/api/config/list`, {
                    timeout: 10000,
                    headers: { 'X-Token': this.jwt }
                }).then(response => {
                    if (response.data) {
                        this.config = response.data
                    }
                })
                .catch(err => (console.log(err)))
        },
        delete_ssid: function(ssid) {
            var i = this.config.network.ssids.indexOf(ssid);
            this.config.network.ssids.splice(i, 1);
            this.update_ssids();
        },
        add_ssid: function() {
            this.config.network.ssids.push(this.ssid);
            this.ssid = "";
            this.update_ssids();
        },
        update_ssids: function() {
            axios.get(`/api/config/edit/network/ssids/${this.config.network.ssids.join("|")}`, {
                    timeout: 10000,
                    headers: { 'X-Token': this.jwt }
                }).then(response => {
                    if (response.data.status) {
                        console.log(response.data)
                    }
                })
                .catch(err => (console.log(err)))
        },
        change_interface: function(type, iface) {
            axios.get(`/api/config/edit/network/${type}/${iface}`, {
                    timeout: 10000,
                    headers: { 'X-Token': this.jwt }
                }).then(response => {
                    if (response.data.status) this.config.network[type] = iface
                })
                .catch(err => (console.log(err)))
        },
    },
    created: function() {
        this.get_jwt().then(() => {
            this.load_config();
        });
    }
}
</script>