<template>
  <div>
    <h3>Node</h3>
    <hr>
    <table class="table">
      <thead>
        <tr>
          <th>Type</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Node ID</td>
          <td>{{node.id}}</td>
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
      </tbody>
    </table>
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