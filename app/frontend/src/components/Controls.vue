<template>
    <div class="controls" v-if="display">
        <i class="off-icon" v-on:click="action('shutdown')" v-if="off_available"></i>
        <i class="quit-icon" v-on:click="action('quit')" v-if="quit_available"></i>
        <i class="update-icon" v-if="update_available&&update_possible" @click="$router.push({ name: 'update' })"></i>
    </div>
</template>
<script>
import axios from 'axios'

export default {
    name: 'Controls',
    data: function (){
        return {
            display: true,
            update_available: false,
            update_possible: false,
            quit_available: false,
            off_available: false
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
        check_update: function() {
            axios.get('/api/update/check', { timeout: 60000 })
            .then(response => { 
              if(response.data.status) {
                if(response.data.message == "A new version is available"){

                  // Allow to show the warning chip.
                  this.update_available = true
                  this.update_possible = true

                  // Pass the versions as "global vars" through window variable.
                  window.current_version = response.data.current_version
                  window.next_version = response.data.next_version
                }
              } else {  
                  this.update_possible = false
              }
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
            if ( ["capture", "report", "update", "loader"].includes(this.$router.currentRoute.name)){
                this.display = false;
            } else {
                this.display = true;
            }
        }
    },
    created: function() {
        this.load_config();
        this.check_update();
    }
}
</script>