<template>
  <div class="container">
    <div style="margin-top:15px;">
      <div class="row">
        <div class="col-10">
          <h3>Teams</h3>
        </div>
        <div class="col-2" style="text-align:right;">
          <!-- <button type="button" class="btn btn-outline-danger" @click="create()">ADD +</button> -->
        </div>
      </div>
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
            <td>{{ team.created  | moment("MMM Do YYYY, HH:mm:ss") }}</td>
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
  methods: {
    create() {
      console.log("hello--")
    }
  }
}
</script>