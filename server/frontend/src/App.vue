<template>
  <div id="app" class="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style>
html {
  background-color: #17191f;
}
.app {
  background-color: #17191f;
  color: white;
  height: 100vh;
}
.navbar {
  background-color: #17191f;
}
.card {
  border: 1px solid #090a15 !important;
  margin: 0 !important;
}
.card-body {
  color: #ff5555;
  background-color: #15171c;
}
.table {
  color: white !important;
}
</style>
