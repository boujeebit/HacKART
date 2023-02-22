<template>
  <div>
    <h3>Node - {{ $props.id }}</h3>
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
            <td>{{node.initialized | moment("MMM Do YYYY, h:mm:ss a") }}</td>
          </tr>
          <tr>
            <td>Hearbeats</td>
            <td>{{node.heartbeats}}</td>
          </tr>
          <tr>
            <td>Heartbeat</td>
            <td>{{node.heartbeat | moment("MMM Do YYYY, h:mm:ss a") }}</td>
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

  export default {
    name: "Node",
    props: ['id'],
    data() {
      return {}
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
    }
  };
</script>