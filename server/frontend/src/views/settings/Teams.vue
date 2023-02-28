<template>
  <div class="container">
    <div style="margin-top:15px;">
      <h3>Teams</h3>
      <hr>
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Created</th>
            <th>Integration</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="team in teams" :keys="team.id">
            <td>{{ team.id }}</td>
            <td>{{ team.name }}</td>
            <td>{{ team.created }}</td>
            <td>{{ team.integration?.name }}</td>
          </tr>
        </tbody>
      </table>
      <!-- {{ teams }} -->
    </div>
  </div>
</template>

<script>
import gql from 'graphql-tag'

export default {
  name: 'Teams',
  data() {
    return {
    }
  },
  apollo: {
    teams: {
      query: gql`
        query{
          teams {
            id
            name
            created
            integration {
              id
              name
            }
          }
        }
      `
    } 
  },
}
</script>