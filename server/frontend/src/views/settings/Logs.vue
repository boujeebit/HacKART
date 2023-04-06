<template>
  <div class="container">
    <div style="margin-top:15px;">
      <h3>Logs</h3>
      <hr>
      <p v-for="log in logs" :key="log.id">{{log}}</p>
    </div>
  </div>
</template>

<script>
  import gql from 'graphql-tag'

  export default {
    name: "Setting_Logs",
    props: ['id'],
    data() {
      return {
      }
    },
    apollo: {
      logs: {
        query: gql`
          query($id: String!) {
            logs(id: $id) {
              id
              code
              message
              timestamp
            }
          }
        `,
        variables () {
          return {
            "id": this.$props.id
          }
        },
        // pollInterval: 5000
      }
    }
  };
</script>

<style>
</style>