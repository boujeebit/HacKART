<template>
  <div>
    <b-container>
      <b-row>
        <b-col style="padding: 0;">
          <b-card title="Nodes" class="mb-2">
            <b-card-text>
              {{ nodeCount }}
            </b-card-text>
          </b-card>
        </b-col>
        <b-col>
          <b-card title="Teams" class="mb-2">
            <b-card-text>
              {{ teamCount }}
            </b-card-text>
          </b-card>
        </b-col>
        <b-col style="padding: 0;">
          <b-card title="Solves" class="mb-2">
            <b-card-text>
              --
            </b-card-text>
          </b-card>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import gql from 'graphql-tag'

export default {
  name: 'HUD',
  apollo: {
    nodeCount: {
      query: gql`
        query{
          nodeCount
        }
      `
    },
    teamCount: {
      query: gql`
        query{
          teamCount
        }
      `
    } 
  },

}
</script>

<style>
</style>