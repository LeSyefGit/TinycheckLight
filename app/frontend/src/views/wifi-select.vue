<template>
    <div :class="[ keyboard == false ? 'center' : '' ]">
        <div v-if="keyboard == false">
            <div v-if="have_internet">
                <p>You seem to be already connected to a network.<br />Do you want to use the current connection?</p>
                <div class="empty-action">
                    <button class="btn" @click="have_internet = false">No, use another</button> <button class="btn" :class="[ connecting ? 'loading' : '', success ? 'btn-success' : 'btn-primary', ]" @click="$router.push({ name: 'generate-ap' })">Yes, use it.</button>
                </div>
            </div>
            <div v-else>
                <div v-if="enter_creds" class="wifi-login">
                    <div class="form-group">
                        <select class="form-select" id="ssid-select" v-model="ssid">
                            <option value="" selected>Wifi name</option>
                            <option v-for="ssid in ssids" v-bind:key="ssid.ssid">
                                {{ ssid.ssid }}
                            </option>
                        </select>
                    </div>
                    <div class="form-group">
                        <input class="form-input" type="password" id="password" v-model="password" placeholder="Wifi password" v-on:click="keyboard = (virtual_keyboard)? true : false">
                    </div>
                    <div class="form-group">
                        <button class="btn width-100" :class="[ connecting ? 'loading' : '', success ? 'btn-success' : 'btn-primary', ]" v-on:click="wifi_setup()">{{ btnval }}</button>
                    </div>
                    <div class="form-group">
                        <button class="btn width-100" :class="[ refreshing ? 'loading' : '' ]" v-on:click="refresh_wifi_list()">Refresh networks list</button>
                    </div>
                </div>
                <div v-else>
                    <p><strong>You seem to not be connected to Internet.</strong><br />Please configure the Wi-Fi connection.</p>
                    <div class="empty-action">
                        <button class="btn btn-primary" @click="enter_creds = true">Ok, let's do that.</button>
                    </div>
                </div>
            </div>
        </div>
        <div v-else>
            <input :value="input" class="keyboardinput" @input="onInputChange" placeholder="Tap on the virtual keyboard to start">
            <SimpleKeyboard @onChange="onChange" @onKeyPress="onKeyPress" :input="input" />
        </div>
    </div>
</template>

<style>
#app {
    overflow-y: hidden;
}   
</style>

<script>
import axios from 'axios'
import router from '../router'
import SimpleKeyboard from "./SimpleKeyboard";

export default {
    name: 'wifi-select',
    components: {
        SimpleKeyboard
    },
    data() {
        return {
            connecting: false,
            error: false,
            success: false,
            btnval: "Connect to it.",
            ssid: "",
            selected_ssid: false,
            password: "",
            keyboard: false,
            input: "",
            ssids: [],
            have_internet: false,
            enter_creds: false,
            virtual_keyboard: false,
            refreshing: false
        }
    },
    props: {
        saved_ssid: String,
        list_ssids: Array,
        internet: Boolean
    },
    methods: {
        wifi_connect: function() {
            axios.get(`/api/network/wifi/connect`, { timeout: 60000 })
                .then(response => {
                    if (response.data.status) {
                        this.success = true
                        this.connecting = false
                        this.btnval = "Wifi connected!"
                        setTimeout(() => router.push('generate-ap'), 1000);
                    } else {
                        this.btnval = "Wifi not connected. Please retry."
                        this.connecting = false
                    }
                })
                .catch(error => {
                    console.log(error)
                });
        },
        wifi_setup: function() {
            if (this.ssid.length && this.password.length >= 8 ){
                axios.post(`/api/network/wifi/setup`, { ssid: this.ssid, password: this.password }, { timeout: 60000 })
                    .then(response => {
                        if(response.data.status) {
                            this.connecting = true
                            this.wifi_connect()
                        } else {
                            console.log(response.data.message)
                        }
                    })
                    .catch(error => {
                        console.log(error)
                    });
            }
        },
        load_config: function() {
            axios.get(`/api/misc/config`, { timeout: 60000 })
                .then(response => {
                    this.virtual_keyboard = response.data.virtual_keyboard
                })
                .catch(error => {
                    console.log(error)
            });
        },
        onChange(input) {
            this.input = input
            this.password = this.input;
        },
        onKeyPress(button) {
            if (button == "{enter}") 
                this.keyboard = false
        },
        onInputChange(input) {
            this.input = input.target.value;
        },
        append_ssids: function(networks) {
            this.ssids = networks
        },
        refresh_wifi_list: function(){
            this.refreshing = true
            axios.get(`/api/network/wifi/list`, { timeout: 10000 })
                 .then(response => { 
                     this.refreshing = false
                     this.append_ssids(response.data.networks)
                 }).catch(error => {
                     this.refreshing = false
                    console.log(error)
            });
        }
    },
    created: function() {
        this.load_config()

        this.have_internet = (this.internet) ? true : false
        this.keyboard = false

        if (typeof this.list_ssids == "object" && this.list_ssids.length != 0){
            this.ssids = this.list_ssids
        } else {
            this.refresh_wifi_list()
        } 
    }
}
</script>
