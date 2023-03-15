<template>
  <div>
    <b-navbar toggleable="lg" type="dark">
      <div class="container">
      <!-- <b-navbar-brand @click="$router.push({ name: 'Dashboard' })" style="cursor: pointer;">HacKART</b-navbar-brand> -->

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <!-- <b-nav-item @click="$router.push({ name: 'Setting_Nodes' })">Nodes</b-nav-item> -->
          <b-nav-item @click="$router.push({ name: 'Setting_Teams' })">Teams</b-nav-item>
          <b-nav-item @click="$router.push({ name: 'Setting_Challenges' })">Challenges</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto">
          <b-nav-item @click="$router.push({ name: 'Setting_Keys' })">Keys</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
      </div>
    </b-navbar>
    <div>
      <router-view></router-view>
    </div>
  </div>
</template>
  
<script>

export default {
  name: "Settings",
  data() {
    return {}
  }
};
</script>