<template>
    <div class="center">
        <p><strong>TinyCheck needs to be updated from the version {{current_version}} to the version {{next_version}}.</strong><br />
            <span v-if="!update_launched">Please click on the button below to update it.</span>
            <span v-else>The process can take few minutes, please wait...</span>
        </p>
        <button class="btn btn-primary" :class="[ update_launched ? 'loading' : '' ]" v-on:click="launch_update()">Update it now</button>
    </div>
</template>

<script>
    import axios from 'axios'

    export default {
        name: 'update',
        data() {
            return {
                translation: {},
                update_launched: null,
                check_interval: null,
                next_version: null,
                current_version: null
            }
        },
        methods: {
            check_update: function() {
                axios.get('/api/update/check-version', { timeout: 60000 })
                .then(response => { 
                    if(response.data.status) {
                        if(response.data.current_version == window.next_version){
                            window.current_version = response.data.current_version
                            clearInterval(this.check_interval);
                            window.location.href = "/";
                        }
                    }
                })
                .catch(error => { console.log(error) });
            },
            launch_update: function() {
                axios.get(`/api/update/process`, { timeout: 60000 })
                .then(response => {
                    if(response.data.status) {
                        if(response.data.message == "Update successfully launched"){
                            this.update_launched = true
                            this.check_interval = setInterval(function(){ this.check_update(); }.bind(this), 3000);
                        }
                    }
                })
                .catch(error => { console.log(error) });
            }
        },
        created: function() {
            if ('next_version' in window && 'current_version' in window){
                if (window.current_version != window.next_version){
                    this.next_version = window.next_version
                    this.current_version = window.current_version
                } else {
                    window.location.href = "/";
                }
            } else {
                window.location.href = "/";
            }

        }
    }
</script>
