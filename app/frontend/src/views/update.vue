<template>
    <div class="center">
        <div v-if="update_possible">
            <div v-if="update_available">
                <p><span class="orange-strong">TinyCheck needs to be updated.</span><br />
                    <span v-if="!update_launched">Please click on the button below to update it.</span>
                    <span v-else>The process can take few minutes, please wait...</span>
                </p>
                <button class="btn btn-primary" :class="[ update_launched ? 'loading' : '' ]" v-on:click="launch_update()">Update it now</button>
            </div>
            <div v-else>
                <p><span class="green-strong">Your TinyCheck instance is up-to-date!</span><br />You'll be redirected in few seconds.</p>
            </div>
        </div>
        <div v-else>
                <p><strong>You dont have Internet or the rights to update Tinycheck.</strong><br />You'll be redirected in few seconds.</p>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'

    export default {
        name: 'update',
        data() {
            return {
                translation: {},
                update_available: null,
                update_possible: true,
                update_launched: null,
                check_interval: null
            }
        },
        methods: {
            check_update: function() {
                axios.get('/api/update/check', { timeout: 60000 })
                .then(response => { 
                    console.log(response.data.status)
                    if(response.data.status) {
                        if(response.data.message == "A new version is available"){
                            this.update_available = true
                            this.update_possible = true
                        } else if (response.data.message == "This is the latest version"){
                            this.update_available = false
                            this.update_possible = true
                            clearInterval(this.check_interval);
                            setTimeout(function () { window.location.href = "/"; }.bind(this), 3000);
                        }
                    } else {
                        this.update_possible = false
                        setTimeout(function () { window.location.href = "/"; }.bind(this), 3000);
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
            this.check_update();
        }
    }
</script>
