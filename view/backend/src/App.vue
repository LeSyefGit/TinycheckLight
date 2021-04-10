<template>
  <div class="backend-container off-canvas off-canvas-sidebar-show">
    <div class="backend-navbar">
      <a class="off-canvas-toggle btn btn-link btn-action" href="#sidebar">
        <i class="icon icon-menu"></i>
      </a>
    </div>
    <div class="backend-sidebar off-canvas-sidebar" id="sidebar">
      <div class="backend-brand">
          <h2 @click="$router.push('/')" class="title">TinyCheck</h2>
      </div>
      <div class="backend-nav">
        <div class="accordion-container">
          <div class="accordion">
            <input id="accordion-configuration" type="checkbox" name="backend-accordion-checkbox" hidden="">
            <label class="accordion-header c-hand" for="accordion-configuration">Manage Device</label>
            <div class="accordion-body">
              <ul class="menu menu-nav">
                <li class="menu-item">
                  <span @click="$router.push('/device/configuration')">Device config</span>
                </li>
                <li class="menu-item">
                  <span @click="$router.push('/device/network')">Network config</span>
                </li>
                <li class="menu-item">
                  <span @click="$router.push('/device/db')">Manage database</span>
                </li>
                <!-- <li class="menu-item">
                  <span @click="$router.push('/device/user')">User configuration</a>
                </li> -->
              </ul>
            </div>
          </div>
          <div class="accordion">
            <input id="accordion-iocs" type="checkbox" name="backend-accordion-checkbox" hidden="">
            <label class="accordion-header c-hand" for="accordion-iocs">Manage IOCs</label>
            <div class="accordion-body">
              <ul class="menu menu-nav">
                <li class="menu-item">
                  <span @click="$router.push('/iocs/manage')">Manage IOCs</span>
                </li>
                <li class="menu-item">
                  <span @click="$router.push('/iocs/search')">Search IOCs</span>
                </li>
              </ul>
            </div>
          </div>
          <div class="accordion">
            <input id="accordion-whitelist" type="checkbox" name="backend-accordion-checkbox" hidden=""/>
            <label class="accordion-header c-hand" for="accordion-whitelist">Manage Whitelist</label>
            <div class="accordion-body">
              <ul class="menu menu-nav">
                <li class="menu-item">
                  <span @click="$router.push('/whitelist/manage')">Manage elements</span>
                </li>
                <li class="menu-item">
                  <span @click="$router.push('/whitelist/search')">Search elements</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <div class="shortcuts">
        <a href="https://github.com/KasperskyLab/tinycheck"><img src="@/assets/github.png" class="shortcut" /></a>
        <a href="https://twitter.com/tinycheck"><img src="@/assets/twitter.png" class="shortcut" /></a>
      </div>
    </div>
    <a class="off-canvas-overlay" href="#close"></a>
    <div class="off-canvas-content">
      <transition name="fade" mode="out-in">
        <router-view/>
      </transition>
    </div>
  </div>
</template>

<script>
  document.title = 'TinyCheck Backend'
</script>
<style>
  @import './assets/spectre.min.css';
  @import './assets/spectre-exp.min.css';
  @import './assets/spectre-icons.min.css';
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