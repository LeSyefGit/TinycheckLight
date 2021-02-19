<template>
    <div class="center">
        <p><strong>TinyCheck needs to be updated to the next version ({{next_version}}).</strong><br />
            <span v-if="!update_launched">Please click on the button below to update it.</span>
            <span v-if="update_launched&&!update_finished">The process can take few minutes, please wait...</span>
            <span v-if="update_launched&&update_finished" class="color-green">✓ Update finished, let's refresh the interface...</span>
        </p>
        <button class="btn btn-primary" :class="[ update_launched ? 'loading' : '' ]" v-on:click="launch_update()" v-if="!update_finished">Update it now</button>
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
                current_version: null,
                update_finished: false
            }
        },
        methods: {
            check_version: function() {
                axios.get('/api/update/get-version', { timeout: 60000 })
                .then(response => { 
                    if(response.data.status) {
                        if(response.data.current_version == window.next_version){
                            window.current_version = response.data.current_version
                            this.update_finished = true
                            clearInterval(this.check_interval);
                            setTimeout(function () { window.location.href = "/"; }, 10000) 
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
                            this.check_interval = setInterval(function(){ this.check_version(); }.bind(this), 1000);
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
