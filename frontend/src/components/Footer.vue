// components/Footer.vue
<template>
  <footer class="footer">
    <p><span class="tagline">Turn communications into strategic insights.</span></p>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter'
}
</script>

<style scoped>
.footer {
  background-color: white;
  padding: 1rem 2rem;
  text-align: center;
  box-shadow: 0 -2px 4px var(--shadow);
  color: var(--secondary);
  font-weight: 500;
}

.tagline {
  color: var(--primary);
  font-style: italic;
}
</style>
