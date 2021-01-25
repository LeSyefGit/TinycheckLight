<template>
    <div class="center">
        <img src="@/assets/logo.png" id="tinycheck-logo" />
        <div class="loading loading-lg loadingsplash"></div>
    </div>
</template>

<script>
    import router from '../router'
    import axios from 'axios'

    export default {
        name: 'splash-screen',
        components: {},
        data() {
            return {
                list_ssids: [],
                internet: false,
                iface_out:""
            }
        },
        methods: {
            // Check if the device is connected to internet.
            internet_check: function() {
                axios.get(`/api/network/status`, { timeout: 10000 })
                    .then(response => {
                        if (response.data.internet){
                            this.internet = true
                        } 
                        this.load_config()
                    })
                    .catch(err => (console.log(err)))
            },
            // Get the WiFi networks around the box.
            get_wifi_networks: function() {
                axios.get(`/api/network/wifi/list`, { timeout: 10000 })
                    .then(response => { 
                        this.list_ssids = response.data.networks
                        this.goto_home();
                     })
                    .catch(err => (console.log(err)))
            },
            // Forward the view to home, with some props 
            // such as (SSIDs, internet & interface)
            goto_home: function() {
                var list_ssids = this.list_ssids
                var internet   = this.internet
                var iface_out  = this.iface_out
                router.replace({ name: 'home', params: { list_ssids: list_ssids, internet: internet, iface_out : iface_out } });
            },
            // Get the network_out from the config
            // to determine the next steps.
            load_config: function() {
                axios.get(`/api/misc/config`, { timeout: 60000 })
                    .then(response => {
                        if(response.data.iface_out){
                            this.iface_out = response.data.iface_out
                            // If ethernet, just goto the homepage.
                            // Else, get wifi networks and then go to home.
                            if(this.iface_out.charAt(0) == "e"){
                                setTimeout(function () { this.goto_home(); }.bind(this), 1000);
                            } else {
                                this.get_wifi_networks();
                            }
                        }
                    })
                    .catch(error => {
                        console.log(error)
                });
            }
        },
        created: function() {
            this.internet_check();
        }
    }
</script>
