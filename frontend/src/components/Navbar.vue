<template>
  <nav class="navbar">
    <div class="logo">
      <i class="fas fa-brain"></i>
      <span>Sentimail - AI Insights</span>
    </div>
    <div class="nav-links">
      <router-link to="/" class="nav-link" exact>Dashboard</router-link>
      <router-link to="/alerts" class="nav-link">Alerts</router-link>
      <router-link to="/sentiment-analysis" class="nav-link">Sentiment Analysis</router-link>
      <router-link to="/subjects" class="nav-link">Subjects</router-link>
    </div>
    <div class="user-actions">
      <button class="btn btn-icon" title="Notifications" @click="goToAlerts">
        <i class="fas fa-bell"></i>
      </button>
      <button class="btn btn-icon" title="Manual Check" @click="checkNow">
        <i class="fas fa-sync" :class="{ 'fa-spin': isChecking }"></i>
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
import simpleService from '@/services/superSimpleService'

export default {
  name: 'AppNavbar',
  data() {
    return {
      isChecking: false
    }
  },
  methods: {
    goToAlerts() {
      this.$router.push('/alerts');
    },
    
    async checkNow() {
      this.isChecking = true;
      console.log('🔄 Manual check triggered');
      await simpleService.checkAndAlert();
      this.isChecking = false;
    }
  },
  
  mounted() {
    console.log('🚀 Starting super simple monitoring');
    simpleService.start();
  }
}
</script>

<style scoped>
.navbar {
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
  position: relative;
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

.fa-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>