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
  background-color: #23272A;
}
.app {
  background-color: #23272A;
  color: white;
  height: 100vh;
}
.navbar {
  background-color: #2C2F33;
}
.card {
  border: 1px solid #992D22 !important;
}
.card-body {
  background-color: #2C2F33;
}
.table {
  color: white !important;
}
</style>
