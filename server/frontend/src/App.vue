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
  background-color: #03030d;
}
.app {
  background-color: #03030d;
  color: white;
  height: 100vh;
}
.navbar {
  background-color: #03030d;
}
.card {
  border: 1px solid #090a15 !important;
  margin: 0 !important;
}
.card-body {
  color: #ff5555;
  background-color: #090a15;
}
.table {
  color: white !important;
}
</style>
