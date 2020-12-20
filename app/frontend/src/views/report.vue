<template>
    <div>
        <div v-if="results">
            <div v-if="alerts.high.length >= 1" class="high-wrapper">
                <div class="center">
                    <h1 class="warning-title">You have {{ nb_translate(alerts.high.length) }} high alert,<br />your device seems to be compromised.</h1>
                    <button class="btn btn-report-low-light" v-on:click="new_capture()">Start a new capture</button>
                    <button class="btn btn-report-high" @click="show_report=true;results=false;">Show the full report</button>
                </div>
            </div>
            <div v-else-if="alerts.moderate.length >= 1" class="med-wrapper">
                <div class="center">
                    <h1 class="warning-title">You have {{ nb_translate(alerts.moderate.length) }} moderate alerts,<br />your device might be compromised.</h1>
                    <button class="btn btn-report-low-light" v-on:click="new_capture()">Start a new capture</button>
                    <button class="btn btn-report-moderate" @click="show_report=true;results=false;">Show the full report</button>
                </div>
            </div>
            <div v-else-if="alerts.low.length >= 1" class="low-wrapper">
                <div class="center">
                    <h1 class="warning-title">You have only {{ nb_translate(alerts.moderate.low) }} low alerts,<br /> don't hesitate to check them.</h1>
                    <button class="btn btn-report-low-light" v-on:click="new_capture()">Start a new capture</button>
                    <button class="btn btn-report-low" @click="show_report=true;results=false;">Show the full report</button>
                </div>
            </div>
            <div v-else  class="none-wrapper">
                <div class="center">
                    <h1 class="warning-title">Everything looks fine, zero alerts.</h1>
                    <button class="btn btn-report-low-light" v-on:click="save_capture()">Save the capture</button>
                    <button class="btn btn-report-low" v-on:click="new_capture()">Start a new capture</button>
                </div>
            </div>
        </div>
        <div v-else-if="show_report" class="report-wrapper">
            <div class="device-ctx">
                <h3 style="margin: 0;">Report for {{device.name}}</h3>
                IP Address: {{device.ip_address}}<br />Mac Address: {{device.mac_address}}
            </div>
            <ul class="alerts">
                <li class="alert" v-for="alert in alerts.high" :key="alert.message">
                    <span class="high-label">High</span><span class="alert-id">{{ alert.id }}</span> 
                    <div class="alert-body">
                        <span class="title">{{ alert.title }}</span>
                        <p class="description">{{ alert.description }}</p>
                    </div>
                </li>
                <li class="alert" v-for="alert in alerts.moderate" :key="alert.message">
                    <span class="moderate-label">Moderate</span><span class="alert-id">{{ alert.id }}</span> 
                    <div class="alert-body">
                        <span class="title">{{ alert.title }}</span>
                        <p class="description">{{ alert.description }}</p>
                    </div>
                </li>
                <li class="alert" v-for="alert in alerts.low" :key="alert.message">
                    <span class="low-label">Low</span><span class="alert-id">{{ alert.id }}</span> 
                    <div class="alert-body">
                        <span class="title">{{ alert.title }}</span>
                        <p class="description">{{ alert.description }}</p>
                    </div>
                </li>
            </ul>
            <div class="columns" id="controls-analysis">
                    <div class="column col-5">
                        <button class="btn width-100" @click="$router.push('generate-ap')">Start a capture</button>
                    </div>
                    <div class="divider-vert column col-2" data-content="OR"></div>
                    <div class="column col-5">
                        <button class="btn btn btn-primary width-100" v-on:click="save_capture()">Save the report</button>
                    </div>
            </div>
        </div>
    </div>
</template>


<style>
#app {
    overflow-y: visible;
}   
</style>

<script>
import router from '../router'

export default {
    name: 'report',   
    data() {
        return {
            results: true,
        }
    },
    props: {
        device: Object,
        alerts: Array,
        capture_token: String
    },
    methods: {
        save_capture: function() {
            var capture_token = this.capture_token
            router.replace({ name: 'save-capture', params: { capture_token: capture_token } });
        },
        new_capture: function() {
            router.push({ name: 'generate-ap' })
        },
        nb_translate: function(x) {
            var nbs = ['zero','one','two','three','four', 'five','six','seven','eight','nine', 'ten', 'eleven']
            try {
                return nbs[x];
            } catch (error)
            {
                return x;
            }
        }
    }
}
</script>
