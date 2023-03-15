<template>
  <div class="container">
    <div style="margin-top:15px;">
      <div class="row">
        <div class="col-10">
          <h3>Challenges</h3>
        </div>
        <div class="col-2" style="text-align:right;">
          <button type="button" class="btn btn-outline-danger">ADD +</button>
        </div>
      </div>
     <hr>
      <table class="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>External ID</th>
            <th>Balloon</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="challenge in challenges" :key="challenge.id">
            <td>{{ challenge.name }}</td>
            <td>{{ challenge.externalId }}</td>
            <td>{{ challenge.balloon }}</td>
            <td><button type="button" class="btn btn-outline-danger" @click="confirmDelete(challenge)">X</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import gql from 'graphql-tag'

export default {
  name: 'Challenges',
  data() {
    return {
      delete: {
        node: null
      }
    }
  },
  apollo: {
    challenges: {
      query: gql`
        query {
          challenges {
            id
            name
            externalId
            balloon
          }
        }
      `
    }
  },
  methods: {
    create() {
      console.log("create.")
      this.$apollo.mutate({
        mutation: gql`
          mutation($action: String!, $id: String, $type: String, $name: String ) {
            integration(action: $action, id: $id, type: $type, name: $name) {
              message
              key
            }
          }
        `,
        variables: {
          "action": "create",
          "type": "HB",
          "name": "SETUP"
        }
      }).then( (data) => {
        console.log(data)
      })
    },
    confirmDelete(challenge) {
      console.log(challenge)
    }
  }
}
</script>