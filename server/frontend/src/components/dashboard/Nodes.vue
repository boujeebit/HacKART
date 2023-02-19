<template>
  <div>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Team</th>
          <th>Heartbeat</th>
          <th>Balloons</th>
          <th>INFO</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="node in nodes" :key="node.id">
          <td>{{node.id}}</td>
          <td>{{node.team?.name}}</td>
          <td>{{node.heartbeat | moment("MMM Do YYYY, h:mm:ss a") }}</td>
          <td>XXX</td>
          <td>info</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import gql from 'graphql-tag'

export default {
  name: 'Nodes',
  apollo: {
    nodes: {
      query: gql`
        query{
          nodes {
            id
            heartbeat
            team {
              id
              name
            }
          }
        }
      `,
      // pollInterval: 5000
    } 
  },

}
</script>

<style>
</style>