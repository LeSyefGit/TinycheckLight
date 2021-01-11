<template>
    <div class="controls">
        <i class="off-icon" v-on:click="action('shutdown')" v-if="off_available && off_display"></i>
        <i class="quit-icon" v-on:click="action('quit')" v-if="quit_available && quit_display"></i>
    </div>
</template>
<script>
import axios from 'axios'
export default {
    name: 'Controls',
    data: function (){
        return {
            off_available : false,
            off_display : false,
            quit_available: false,
            quit_display : false
            }
    },
    methods: {
        action: function(action) {
            axios.get(`/api/misc/${action}`, { timeout: 30000 })
            .then(response => {
                if(response.data.status)
                    console.log(`Let's ${action}`)
            })
            .catch(error => { console.log(error) });
        },
        load_config: function() {
            axios.get(`/api/misc/config`, { timeout: 60000 })
            .then(response => {
                this.quit_available = response.data.quit_option
                this.off_available = response.data.shutdown_option
            })
            .catch(error => { console.log(error) });
        }
    },
    watch: {
        $route (){
            if ( ["capture", "report"].includes(this.$router.currentRoute.name) || screen.height != window.innerHeight ){
                this.off_display = false;
                this.quit_display = false;
            } else {
                this.off_display = (this.off_available)? true : false;
                this.quit_display = (this.quit_available)? true : false;
            }
        }
    },
    created: function() {
        this.load_config()
    },
}
</script>