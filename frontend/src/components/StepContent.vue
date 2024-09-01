<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <h3>{{ title }}</h3>
  <div class="body">
    <slot></slot>
  </div>
</template>

<style scoped>
.body {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  height: 100%;
  overflow: auto;
  box-sizing: border-box;
  padding: 0.2rem 0rem;
}
</style>
