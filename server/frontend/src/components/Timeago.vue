<template>
  <span>
    {{ timeSince }}
  </span>
</template>

<script>

export default {
  name: 'Timeago',
  props: ['date'],
  data() {
    return {
      timeSince: null
    }
  },
  created() {
    this.timeSince = this.$moment(this.date).fromNow()
    setInterval( () => {
      this.timeSince = this.$moment(this.date).fromNow()
    }, 5000)
  }
}
</script>

<style>
</style>