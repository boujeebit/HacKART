<template>
  <div class="container">
    <div style="margin-top:15px;">
    <div class="row">
      <div class="col-10">
        <h3>Node ({{ node.name }})</h3>
      </div>
      <div class="col-2" style="text-align:right;">
        <button type="button" class="btn btn-outline-danger" @click="blinky()">Blinky</button>
        <br>
        <span v-if="blinky_data.running">Command Sent</span>
        <span v-if="blinky_data.result">Result: {{ blinky_data.result }}</span>

      </div>
    </div>
    

    <fieldset class="scheduler-border">
      <legend class="scheduler-border">Node</legend>
      <div v-if="!$apollo.queries.node.loading">
      <table class="table">
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
        </tbody>
      </table>
    </div>
    </fieldset>


    <fieldset class="scheduler-border">
      <legend class="scheduler-border">Networking</legend>
      <div v-if="!$apollo.queries.node.loading">
      <table class="table">
        <tbody>
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
        </tbody>
      </table>
    </div>
    </fieldset>


    <fieldset class="scheduler-border">
      <legend class="scheduler-border">Solves</legend>
      <div v-for="solve in node.solves" :key="solve.id">
        {{ solve.challenge.name }} // {{ solve.time }} //{{ solve.challenge.balloon }}
      </div>
    </fieldset>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
  </div>
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
              name
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
                time
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

<style>
fieldset.scheduler-border {
    border: 1px groove #ddd !important;
    padding: 0 1.4em 1.4em 1.4em !important;
    margin: 0 0 1.5em 0 !important;
    -webkit-box-shadow:  0px 0px 0px 0px #000;
            box-shadow:  0px 0px 0px 0px #000;
}

legend.scheduler-border {
    font-size: 1.2em !important;
    font-weight: bold !important;
    text-align: left !important;
    width:inherit; /* Or auto */
    padding:0 10px; /* To give a bit of padding on the left and right */
    border-bottom:none;
}
</style>