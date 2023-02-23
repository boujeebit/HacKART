<template>
  <div>
    <div class="row">
      <div class="col-10">
        <h3>Node <span style="font-size: small;">({{ $props.id }})</span></h3>
      </div>
      <div class="col-2" style="text-align:right;">
        <button type="button" class="btn btn-outline-danger" @click="blinky()">Blinky</button>
        <br>
        <span v-if="blinky_data.running">Command Sent</span>
        <span v-if="blinky_data.result">Result: {{ blinky_data.result }}</span>

      </div>
    </div>
    
    <hr>

    <div v-if="!$apollo.queries.node.loading">
      <table class="table">
        <thead>
          <tr>
            <th>Type</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>HacKART ID</td>
            <td>{{node.id}}</td>
          </tr>
          <tr>
            <td>Machine ID</td>
            <td>{{node.machineid}}</td>
          </tr>
          <tr>
            <td>Initialized</td>
            <td>{{node.initialized | moment("MMM Do YYYY, h:mm:ss a") }} || <timeago v-if="node.initialized" :date="node.initialized" :key="node.initialized"></timeago> </td>
          </tr>
          <tr>
            <td>Hearbeats</td>
            <td>{{node.heartbeats}}</td>
          </tr>
          <tr>
            <td>Heartbeat</td>
            <td>{{node.heartbeat | moment("MMM Do YYYY, h:mm:ss a") }} || <timeago v-if="node.heartbeat" :date="node.heartbeat" :key="node.heartbeat"></timeago> </td>
          </tr>
          <tr>
            <td>Interval</td>
            <td>{{node.internval}}</td>
          </tr>
          <tr>
            <td></td>
            <td></td>
          </tr>
          <tr>
            <td>MAC</td>
            <td>{{node.networking?.mac}}</td>
          </tr>
          <tr>
            <td>IP Address</td>
            <td>{{node.networking?.address}}</td>
          </tr>
          <tr>
            <td>Subnet mask</td>
            <td>{{node.networking?.subnet}}</td>
          </tr>
          <tr>
            <td>Default Gateway</td>
            <td>{{node.networking?.gateway}}</td>
          </tr>
          <tr>
            <td>DNS</td>
            <td>{{node.networking?.dns}}</td>
          </tr>
          <tr>
            <td></td>
            <td></td>
          </tr>
          <tr>
            <td>Solves</td>
            <td>{{node.solves}}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      Loading
    </div>
    <!-- {{ node }} -->
  </div>
</template>

<script>
  import gql from 'graphql-tag'
  import Timeago from '../components/Timeago.vue';

  export default {
    name: "Node",
    props: ['id'],
    components: {
      Timeago
    },
    data() {
      return {
        blinky_data: {
          running: false,
          result: null
        }
      }
    },
    apollo: {
      node : {
        query: gql`
          query($id: String!) {
            node(id: $id) {
              id
              machineid
              initialized
              heartbeats
              heartbeat
              internval
              networking {
                mac
                address
                subnet
                gateway
                dns
              }
              solves {
                challenge {
                  name
                  balloon
                }
              }
            }
          }
        `,
        variables () {
          return {
            "id": this.$props.id
          }
        },
        pollInterval: 5000
      }
    },
    methods: {
      blinky() {
        this.blinky_data.result = null
        this.blinky_data.running = true
        let self = this
        this.$apollo.query({
          query: gql`
            query {
              blinky
            }
          `
        }).then((data) => {
          console.log(data.data)
          self.blinky_data.running = false
          self.blinky_data.result = data.data.blinky
        })
      }
    }
  };
</script>