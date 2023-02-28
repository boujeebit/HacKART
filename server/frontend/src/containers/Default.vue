<template>
    <div>
  <b-navbar toggleable="lg" type="dark">
    <div class="container">
    <b-navbar-brand @click="$router.push({ name: 'Dashboard' })" style="cursor: pointer;">HacKART</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <!-- <b-nav-item href="#">Teams</b-nav-item> -->
        
      </b-navbar-nav>

      <b-navbar-nav class="ml-auto">
        <b-nav-item @click="$router.push({ name: 'Settings' })">Settings</b-nav-item>
        <b-nav-item-dropdown right>
          <!-- Using 'button-content' slot -->
          <template #button-content>
            <em>{{identity?.firstName}} {{identity?.lastName}}</em>
          </template>
          <!-- <b-dropdown-item href="#">Profile</b-dropdown-item> -->
          <b-dropdown-item @click="logout">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
    </div>
  </b-navbar>
    <!-- <div class="container">
        <div style="margin-top:15px;"> -->
            <router-view></router-view>
        <!-- </div>
    </div> -->
    </div>
</template>

<script>
import gql from 'graphql-tag'

export default {
  name: 'Default',
  apollo: {
    identity: {
      query: gql`
        query{
          identity {
            firstName
            lastName
          }
        }
      `
    } 
  },
  methods: {
    logout() {
      let self = this;
      this.$apollo.mutate({
        mutation: gql`
          mutation { 
            logout { 
              status 
            } 
          }
        `
      }).then( (data) => {
        self.$router.push({ name: "Login" });
      })
    }
  }
}
</script>

<style>
</style>