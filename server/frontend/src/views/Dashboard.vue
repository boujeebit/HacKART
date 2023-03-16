<template>
  <div class="container">
    <div style="margin-top:15px;">
      <HUD/>
      <br>
      <BarChart/>
      <br>
      <nodes/>
    </div>
  </div>
</template>

<script>
import HUD from '../components/dashboard/HUD.vue';
import BarChart from '../components/dashboard/BarChart.vue';
import Nodes from '../components/dashboard/Nodes.vue';

export default {
  name: "Dashboard",
  components: {
    HUD,
    BarChart,
    Nodes
  },
  data() {
    return {}
  }
};
</script>