<template>
  <div>
    <div style="text-align:right;">
      <!-- <button class="btn btn-add">Create Node </button> -->
    </div>
    
    <table class="table">
      <thead>
        <tr>
          <th></th>
          <th>Name</th>
          <th>Team</th>
          <th>Initialized</th>
          <th>Heartbeat</th>
          <th style="text-align: right;">Balloons</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="node in nodes" :key="node.id" @click="$router.push({ name: 'Node', params: {id: node.id} })" style="cursor: pointer;">
          <td>
            <template v-if="!node.state && node.team?.state">
              <font-awesome-icon class="balloon-danger" icon="fa-solid fa-triangle-exclamation"/>
            </template>
            <template v-else-if="!node.state || !node.team?.state">
              <font-awesome-icon class="balloon-warn" icon="fa-solid fa-triangle-exclamation"/>
            </template>
            <template v-else-if="node.team?.state">
              <font-awesome-icon v-if="JSON.parse(node.state).A === JSON.parse(node.team.state).A && JSON.parse(node.state).B === JSON.parse(node.team.state).B && JSON.parse(node.state).C === JSON.parse(node.team.state).C" class="balloon-success" icon="fa-solid fa-square-check"/>
              <font-awesome-icon v-else class="balloon-danger" icon="fa-solid fa-triangle-exclamation"/>
            </template>
          </td>
          <td v-b-tooltip.hover.left :title="'UUID: '+node.id">{{node.name}}</td>
          <td>{{node.team?.name}}</td>
          <td v-if="node.initialized">{{node.initialized | moment("MMM Do YYYY, h:mm:ss a") }}</td>
          <td v-else><i>Never seen...</i></td>
          <td v-if="node.heartbeat">{{node.heartbeat | moment("MMM Do YYYY, h:mm:ss a") }}</td>
          <td v-else><i>Never seen...</i></td>
          <td style="text-align: right;">
            <!-- {{ node.state }} -- {{ node.team?.state }} -->
            <!-- Universal Unknown state -->
            <template v-if="!node.state && !node.team?.state">
              <font-awesome-icon class="status balloon-warn icon-border-warn" icon="fa-circle-question"/>
              <font-awesome-icon class="status balloon-warn icon-border-warn" icon="fa-circle-question" />
              <font-awesome-icon class="status balloon-warn icon-border-warn" icon="fa-circle-question" />
            </template>

            <!-- Team State but no Node State -->
            <template v-if="!node.state && node.team?.state">
              <font-awesome-icon :class="JSON.parse(node.team.state).A ? 'icon-border-success' : 'icon-border-danger'" class="status balloon-warn" icon="fa-circle-question"/>
              <font-awesome-icon :class="JSON.parse(node.team.state).B ? 'icon-border-success' : 'icon-border-danger'" class="status balloon-warn" icon="fa-circle-question" />
              <font-awesome-icon :class="JSON.parse(node.team.state).C ? 'icon-border-success' : 'icon-border-danger'" class="status balloon-warn" icon="fa-circle-question" />
            </template>

            <!-- Node State known but no team -->
            <template v-else-if="node.state && !node.team?.state">
              <font-awesome-icon :class="JSON.parse(node.state).A ? 'balloon-success' : 'balloon-danger'" class="status icon-border-warn"  icon="fa-circle-question" />
              <font-awesome-icon :class="JSON.parse(node.state).B ? 'balloon-success' : 'balloon-danger'" class="status icon-border-warn"  icon="fa-circle-question" />
              <font-awesome-icon :class="JSON.parse(node.state).C ? 'balloon-success' : 'balloon-danger'" class="status icon-border-warn"  icon="fa-circle-question" />
            </template>
            
            <!-- Node and team state known -->
            <template v-else-if="node.state && node.team?.state">
              <font-awesome-icon :class="[(JSON.parse(node.state).A ? 'balloon-success' : 'balloon-danger'), (JSON.parse(node.team.state).A ? 'icon-border-success' : 'icon-border-danger')]" class="status" :icon="JSON.parse(node.state).A === JSON.parse(node.team.state).A ? 'fa-solid fa-circle-check' : 'fa-solid fa-circle-exclamation'" />
              <font-awesome-icon :class="[(JSON.parse(node.state).B ? 'balloon-success' : 'balloon-danger'), (JSON.parse(node.team.state).B ? 'icon-border-success' : 'icon-border-danger')]" class="status" :icon="JSON.parse(node.state).B === JSON.parse(node.team.state).B ? 'fa-solid fa-circle-check' : 'fa-solid fa-circle-exclamation'" />
              <font-awesome-icon :class="[(JSON.parse(node.state).C ? 'balloon-success' : 'balloon-danger'), (JSON.parse(node.team.state).C ? 'icon-border-success' : 'icon-border-danger')]" class="status" :icon="JSON.parse(node.state).C === JSON.parse(node.team.state).C ? 'fa-solid fa-circle-check' : 'fa-solid fa-circle-exclamation'" />
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
            initialized
            state
            team {
              id
              name
              state
            }
          }
        }
      `,
      pollInterval: 5000
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

.balloon-warn {
  color: #ffb86c
}

.balloon-success {
  color: #50fa7b
}

.balloon-danger {
  color: #ff5555;
}

.icon-border-warn {
  border-radius: 50%;
  border: 2px solid #ffb86c;
}

.icon-border-success {
  border-radius: 50%;
  border: 2px solid #50fa7b;
}

.icon-border-danger {
  border-radius: 50%;
  border: 2px solid #ff5555;
}
</style>