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
  document.title = 'TinyCheck Frontend'
  import Controls from "@/components/Controls.vue"

  export default {
    name: 'app',
    components: {
        Controls
    }
  }
</script>

