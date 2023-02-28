<template>
  <div>
    <div style="text-align:right;">
      <button class="btn btn-add">Create Node </button>
    </div>
    
    <table class="table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Team</th>
          <th>Heartbeat</th>
          <th style="text-align: right;">Balloons</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="node in nodes" :key="node.id" @click="$router.push({ name: 'Node', params: {id: node.id} })" style="cursor: pointer;">
          <td v-b-tooltip.hover.left :title="'UUID: '+node.id">{{node.name}}</td>
          <td>{{node.team?.name}}</td>
          <td v-if="node.heartbeat">{{node.heartbeat | moment("MMM Do YYYY, h:mm:ss a") }}</td>
          <td v-else></td>
          <td style="text-align: right;">
            <template v-if="!node.heartbeat">
              <font-awesome-icon class="status" style="color:#ffb86c" icon="fa-circle-question"/>
              <font-awesome-icon class="status" style="color:#ffb86c" icon="fa-circle-question" />
              <font-awesome-icon class="status" style="color:#ffb86c" icon="fa-circle-question" />
            </template>
            <template v-else>
              <font-awesome-icon v-if="JSON.parse(node.balloons).b1" class="status" style="color:#ff5555" icon="fa-solid fa-circle" />
              <font-awesome-icon v-else class="status" style="color:#50fa7b" icon="fa-solid fa-circle" />

              <font-awesome-icon v-if="JSON.parse(node.balloons).b2" class="status" style="color:#ff5555" icon="fa-solid fa-circle" />
              <font-awesome-icon v-else class="status" style="color:#50fa7b" icon="fa-solid fa-circle" />

              <font-awesome-icon v-if="JSON.parse(node.balloons).b3" class="status" style="color:#ff5555" icon="fa-solid fa-circle" />
              <font-awesome-icon v-else class="status" style="color:#50fa7b" icon="fa-solid fa-circle" />
              <!-- <font-awesome-icon class="status" style="color:#50fa7b" icon="fa-solid fa-circle-exclamation" />
              <font-awesome-icon class="status" style="color:#50fa7b" icon="fa-solid fa-circle-check" /> -->
            </template>
          </td>
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
            name
            heartbeat
            team {
              id
              name
            }
            balloons
          }
        }
      `,
      // pollInterval: 5000
    } 
  },

}
</script>

<style>
.btn-add {
  color: #ff5555;
  background-color: #34373d;
  /* border: 1px solid #ff5555; */
  margin-bottom: 15px;
}
            
.status {
  margin:0 5px 0 5px;
}

.table thead th {
    vertical-align: bottom;
    border-bottom: 2px solid #34373d !important;
}
.table th, .table td {
    padding: 0.75rem;
    vertical-align: top;
    border-top: 1px solid #34373d !important;
}
</style>