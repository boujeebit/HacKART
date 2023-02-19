<template>
  <div>
    <h3>Dashboard</h3>
    <hr>
    <b-container>
      <b-row>
        <b-col>
          <b-card title="Nodes" class="mb-2">
            <b-card-text>
              
            </b-card-text>
          </b-card>
        </b-col>
        <b-col>
          <b-card title="Teams" class="mb-2">
            <b-card-text>
              
            </b-card-text>
          </b-card>
        </b-col>
        <b-col>
          <b-card title="Solves" class="mb-2">
            <b-card-text>
              
            </b-card-text>
          </b-card>
        </b-col>
      </b-row>
    </b-container>

    <br>
    <nodes/>
  </div>
</template>

<script>
import Nodes from '../components/Nodes.vue';

export default {
  name: "Dashboard",
  components: {
    Nodes
  },
  data() {
    return {}
  }
};
</script>