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
    props: { saved_ssid: String, list_ssids: Array, internet: Boolean },
    methods: {
        next: function() {
            var saved_ssid = this.saved_ssid
            var list_ssids = this.list_ssids
            var internet = this.internet
            router.push({ name: 'wifi-select', params: { saved_ssid: saved_ssid, list_ssids: list_ssids, internet:internet } });
        }
    }
}
</script>
