<template>
  <div class="app">
    <AppNavbar />
    <main class="main-content">
      <router-view />
    </main>
    <AppFooter />
  </div>
</template>

<script>
import AppNavbar from './components/Navbar.vue'
import AppFooter from './components/Footer.vue'

export default {
  name: 'App',
  components: {
    AppNavbar,
    AppFooter
  }
}
</script>

<style>
:root {
  --primary: #3366CC;
  --secondary: #7F8FA6;
  --accent: #00B8D9;
  --background: #F7F9FC;
  --text: #2D3748;
  --shadow: rgba(0, 0, 0, 0.1);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

body {
  background-color: var(--background);
  color: var(--text);
  min-height: 100vh;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 2rem;
  background-color: var(--background);
}
</style>