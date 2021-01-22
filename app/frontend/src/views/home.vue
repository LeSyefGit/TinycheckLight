<template>
    <div class="center">
        <h3 class="lobster">Welcome to TinyCheck.</h3>
        <p>We are going to help you to check your device.</p>
        <button class="btn btn-primary" v-on:click="next()">Let's start!</button>
    </div>
</template>

<script>
import router from '../router'

export default {
    name: 'home',
    props: { saved_ssid: String, iface_out: String, list_ssids: Array, internet: Boolean },
    methods: {
        next: function() {
            var saved_ssid = this.saved_ssid
            var list_ssids = this.list_ssids
            var internet = this.internet
            console.log(this.iface_out)
            if (this.iface_out.charAt(0) == "e"){
                router.push({ name: 'generate-ap' });
            } else {
                router.push({ name: 'wifi-select', 
                              params: { saved_ssid: saved_ssid, 
                                        list_ssids: list_ssids, 
                                        internet:internet } });
            }
               }
    }
}
</script>
