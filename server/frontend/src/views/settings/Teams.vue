<template>
  <div class="container">
    <div style="margin-top:15px;">
      <h3>Teams</h3>
      <hr>
      <table class="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>External ID</th>
            <th>Created</th>
            <th>Integration</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="team in teams" :keys="team.id">
            <td>{{ team.name }}</td>
            <td>{{ team.externalId }}</td>
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
            externalId
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