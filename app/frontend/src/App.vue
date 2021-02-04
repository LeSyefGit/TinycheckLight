<template>
  <div id="app">
    <div class="wrapper">
      <Controls />
      <transition name="fade" mode="out-in">
        <router-view />
      </transition>
    </div>
  </div>
</template>

<style>
  @import './assets/spectre.min.css';
  @import './assets/custom.css';
  
  /* Face style for router stuff. */
  .fade-enter-active,
  .fade-leave-active {
    transition-duration: 0.3s;
    transition-property: opacity;
    transition-timing-function: ease;
  }

  .fade-enter,
  .fade-leave-active {
    opacity: 0
  }
</style>

<script>
  import axios from 'axios'
  document.title = 'TinyCheck Frontend'
  import Controls from "@/components/Controls.vue"
  
  export default {
    name: 'app',
    components: {
        Controls
    },
    methods: {
        get_lang: function() {
            axios.get(`/api/misc/get-lang`, { timeout: 60000 })
                .then(response => { window.translation = response.data; })
                .catch(error => { console.log(error) });
        }
    },
    created: function() {
        window.translation = {}
        this.get_lang()
    }
  }
</script>

