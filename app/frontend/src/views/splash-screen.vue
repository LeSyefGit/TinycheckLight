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
                internet: false
            }
        },
        methods: {
            // Check if the device is already connected to internet.
            internet_check: function() {
                axios.get(`/api/network/status`, { timeout: 10000 })
                    .then(response => {
                        if (response.data.internet) this.internet = true
                        this.get_wifi_networks()
                    })
                    .catch(err => (console.log(err)))
            },
            // Get the WiFi networks around the box.
            get_wifi_networks: function() {
                axios.get(`/api/network/wifi/list`, { timeout: 10000 })
                    .then(response => (this.append_ssids(response.data.networks)))
                    .catch(err => (console.log(err)))
            },
            // Handle the get_wifi_networks answer and call goto_home.
            append_ssids: function(networks) {
                this.list_ssids = networks
                this.goto_home()
            },
            // Pass the list of ssids and the internet status as a prop to the home view.
            goto_home: function() {
                var list_ssids = this.list_ssids
                var internet = this.internet
                router.replace({ name: 'home', params: { list_ssids: list_ssids, internet: internet } });
            }
        },
        created: function() {
            this.internet_check();
        }
    }
</script>
