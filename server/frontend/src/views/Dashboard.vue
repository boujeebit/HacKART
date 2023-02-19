<template>
  <div>
    <h3>Dashboard</h3>
    <hr>
    <HUD/>
    <br>
    <nodes/>
  </div>
</template>

<script>
import HUD from '../components/dashboard/HUD.vue';
import Nodes from '../components/dashboard/Nodes.vue';

export default {
  name: "Dashboard",
  components: {
    HUD,
    Nodes
  },
  data() {
    return {}
  }
};
</script>