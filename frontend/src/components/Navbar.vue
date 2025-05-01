// components/Navbar.vue
<template>
  <nav class="navbar">
    <div class="logo">
      <i class="fas fa-brain"></i>
      <span>AI Insights</span>
    </div>
    <div class="nav-links">
      <router-link to="/" class="nav-link" exact>Dashboard</router-link>
      <router-link to="/reports" class="nav-link">Reports</router-link>
      <router-link to="/analytics" class="nav-link">Analytics</router-link>
      <router-link to="/settings" class="nav-link">Settings</router-link>
    </div>
    <div class="user-actions">
      <button class="btn btn-icon" title="Notifications">
        <i class="fas fa-bell"></i>
      </button>
      <button class="btn btn-icon" title="Help">
        <i class="fas fa-question-circle"></i>
      </button>
      <div class="user-profile" title="User Profile">
        M
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'AppNavbar'
}
</script>

<style scoped>
.navbar {
  background-color: white;
  box-shadow: 0 2px 4px var(--shadow);
  padding: 0.75rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  font-size: 1.25rem;
  color: var(--primary);
}

.logo i {
  font-size: 1.5rem;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  text-decoration: none;
  color: var(--text);
  font-weight: 500;
  transition: color 0.3s;
}

.nav-link:hover {
  color: var(--primary);
}

.nav-link.router-link-active {
  color: var(--primary);
  border-bottom: 2px solid var(--primary);
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.btn {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text);
  transition: color 0.3s;
}

.btn:hover {
  color: var(--primary);
}

.btn-icon {
  font-size: 1.25rem;
  padding: 0.5rem;
  border-radius: 50%;
}

.user-profile {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  background-color: var(--secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
}

@media (max-width: 768px) {
  .navbar {
    padding: 0.75rem 1rem;
    flex-wrap: wrap;
  }
  
  .nav-links {
    order: 3;
    width: 100%;
    justify-content: space-around;
    margin-top: 0.75rem;
    gap: 0.5rem;
  }
}
</style>