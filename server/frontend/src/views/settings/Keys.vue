<template>
  <div class="container">
    <div style="margin-top:15px;">
      <div class="row">
        <div class="col-10">
          <h3>Keys</h3>
        </div>
        <div class="col-2" style="text-align:right;">
          <!-- <button type="button" class="btn btn-outline-danger" @click="create()">ADD +</button> -->
          <button type="button" class="btn btn-outline-danger" @click="mangament.edit = !mangament.edit">Edit</button>
          <button v-if="mangament.edit" type="button" class="btn btn-outline-danger" @click="mangament.add = !mangament.add">ADD +</button>
        </div>
      </div>
      <div v-if="mangament.add">
        <h3>Add</h3>
        <b-form inline>
          <b-form-select
            id="inline-form-custom-select-pref"
            class="mb-2 mr-sm-2 mb-sm-0"
            :options="[{ text: 'Type...', value: null }, { text: 'Heartbeat', value: 'HB' }, { text: 'Platform', value: 'PF' }]"
            :value="null"
            v-model="newKey.type"
          ></b-form-select>

          <label class="sr-only" for="inline-form-input-name">Name</label>
          <b-form-input v-model="newKey.name" id="inline-form-input-name" class="mb-2 mr-sm-2 mb-sm-0" placeholder="Name.."></b-form-input>

          <b-button variant="primary" @click="create()">Create</b-button>
        </b-form>
        <p v-if="newKey.key">This is the only time you will be able to see your API key. Your API Key is: <code>{{ newKey.key }}</code>.</p>
      </div>
      <hr>
      <hr>
      <table class="table">
        <thead>
          <tr>
            <th>Type</th>
            <th>Name</th>
            <th>ID</th>
            <th>Key</th>
            <th>Created</th>
            <th>Created By</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="integration in integrations" :key="integration.id" @click="$router.push({ name: 'Setting_Logs', params: {id: integration.id} })" style="cursor: pointer;">
            <td>{{ integration.type }}</td>
            <td>{{ integration.name }}</td>
            <td>{{ integration.id }}</td>
            <td>{{ integration.hint }}</td>
            <td>{{ integration.created  | moment("MMM Do YYYY, HH:mm:ss") }}</td>
            <td>{{ integration.createdBy.firstName }} {{ integration.createdBy.lastName }}</td>
            <td>
              <!-- <button v-if="mangament.edit" type="button" class="btn btn-outline-danger">D</button> -->
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import gql from 'graphql-tag'

export default {
  name: 'Keys',
  data() {
    return {
      mangament: {
        edit: false,
        add: false
      },
      newKey: {
        name: null,
        type: null,
        key: null
      }
    }
  },
  apollo: {
    integrations: {
      query: gql`
      query {
        integrations {
          id
          name
          hint
          type
          created
          createdBy {
            firstName
            lastName
          }
        }
      }
      `
    }
  },
  methods: {
    create() {
      console.log("create.")
      console.log(this.newKey)
      let self = this
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
          "type": self.newKey.type,
          "name": self.newKey.name
        }
      }).then( (data) => {
        self.newKey.key = data.data.integration.key
      })
    }
  }
}
</script>