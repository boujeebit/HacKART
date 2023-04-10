<template>
  <div class="container">
    <div style="margin-top:15px;">
    <div class="row">
      <div class="col-10">
        <h3>Node ({{ node?.name }})</h3>
      </div>
      <div class="col-2" style="text-align:right;">
        <b-button v-b-modal.modal-1>Sync</b-button>
      </div>
    </div>
    

    

    <b-modal id="modal-1" title="Synchronize State" @ok="handleSync">
      <b-form-select
        id="inline-form-custom-select-pref"
        class="mb-2 mr-sm-2 mb-sm-0"
        :options="[{ text: 'Select Action', value: null }, { text: 'Reset Board', value: 1 }, { text: 'Team Sync', value: 2 }, { text: 'Custom', value: 3 }]"
        :value="null"
        v-model="syncData.action"
      ></b-form-select>
      <div v-if="syncData.action">
        <hr>
        <div v-if="syncData.action === 1">
          <p>Reseting the board puts all relays in the off position. To continue click okay.</p>
        </div>
        <div v-if="syncData.action === 2">
          <p>Team Sync synchronizes the curent team state with the board. This does not pop any balloons even if the board is reporting it as available. To continue click okay.</p>
        </div>
        <div v-if="syncData.action === 3">
          <b-form-select
          id="inline-form-custom-select-pref"
          class="mb-2 mr-sm-2 mb-sm-0"
          :options="[{ text: 'Action...', value: null }, { text: 'Sync', value: 1 }, { text: 'Pop', value: 2 }]"
          :value="null"
          v-model="syncData.custom"
        ></b-form-select>
        <p v-if="syncData.custom === 1"><code>Sync</code> will sync the state but not pop any balloons. Enabling balloons that are availble on the board will put the balloon in a blocking state and team solves will not have any effect (a.k.a balloon will not be popped).</p>
        <p v-if="syncData.custom === 2"><code>Pop</code> will sync the state and <strong>pop</strong> balloons if the board is reporting it as available.</p>

        <div v-if="syncData.custom">
        
        <b-form-group>
          <b-form-checkbox-group
            v-model="syncData.selected"
            :options="syncData.options"
            switches
          ></b-form-checkbox-group>
        </b-form-group>
        <hr>
        <p>Last heartbeat board state: </p>
        <code>{{ node.state }}</code>
        </div>
        <hr>
        <div v-if="syncData.response === true">
          Sync was successfully acknowledged by the broker. 
        </div>
        <div v-else-if="syncData.response === false">
          Broker error.
        </div>
      </div>
        
        
      </div>
    </b-modal>


    <div v-if="showSync" style="margin-bottom: 45px;">
      <h6>Sync</h6>
      <b-form inline>
        <b-form-select
          id="inline-form-custom-select-pref"
          class="mb-2 mr-sm-2 mb-sm-0"
          :options="[{ text: 'Type...', value: null }, { text: 'Pop', value: 'pop' }, { text: 'Sync', value: 'sync' }]"
          :value="null"
          v-model="syncData.type"
        ></b-form-select>

        <b-form-group>
          <b-form-checkbox-group
            v-model="syncData.selected"
            :options="syncData.options"
            switches
          ></b-form-checkbox-group>
        </b-form-group>
      </b-form>
      <b-button variant="primary" @click="sync()">Send</b-button>
    </div>

    <fieldset class="scheduler-border">
      <legend class="scheduler-border">Team</legend>
      <div v-if="!$apollo.queries.node.loading">
        <div v-if="node.team">
          Team name: {{ node.team.name }}
          <hr>
          <div v-for="solve in node.team.solves">
            Solved: {{ solve.challenge.name }} // {{ solve.time }}
          </div>
        </div>
        <div v-else>
          No Team
        </div>

    </div>
    </fieldset>

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
            <td>SSID</td>
            <td>{{node.networking?.ssid}}</td>
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
        </tbody>
      </table>
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
        showSync: false,
        syncData: {
          action: null,
          selected: [],
          options: [
            { text: 'A', value: 'A' },
            { text: 'B', value: 'B' },
            { text: 'C', value: 'C' }
          ],
          custom: null,
          response: null
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
              state
              networking {
                ssid
                mac
                address
                subnet
                gateway
                dns
              }
              team {
                id
                name
                solves {
                  id
                  time
                  challenge {
                    name
                  }
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
        // pollInterval: 5000
      }
    },
    methods: {
      handleSync(bvModalEvent) {
        bvModalEvent.preventDefault()
        let self = this;
        let a = false
        let b = false
        let c = false
        let action  = null
        let enforce = false
        // Reset board 
        if (this.syncData.action === 1) {
          action = 'reset'
        } else if (this.syncData.action === 2) {
          action = 'team'
        } else if (this.syncData.action === 3) {
          action = 'custom'
          for (let i = 0; i < this.syncData.selected.length ; i++) {
            if (this.syncData.selected[i] === 'A') {
              a = true
            } else if (this.syncData.selected[i] === 'B') {
              b = true
            } else if (this.syncData.selected[i] === 'C') {
              c = true
            }
          }
        } else {
          console.log("Bad input. User validation.")
          return
        }

        if (this.syncData.custom === 2) {
          enforce = true
        }

        this.$apollo.query({
          query: gql`
            query($id: String!, $action: String!, $enforce: Boolean, $a: Boolean, $b: Boolean, $c: Boolean ) {
              sync(id: $id, action: $action, enforce: $enforce, a: $a, b: $b, c: $c)
            }
          `,
          variables: {
            "id": this.node.id,
            "action": action,
            "enforce": enforce,
            "a": a,
            "b": b,
            "c": c
          },
          fetchPolicy: 'no-cache'
        }).then((data) => {
          console.log(data.data)
          self.syncData.response = data.data.sync
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