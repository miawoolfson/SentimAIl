<template>
  <nav class="navbar">
    <div class="logo">
      <i class="fas fa-brain"></i>
      <span>Sentimail - AI Insights</span>
    </div>
    <div class="nav-links">
      <router-link to="/" class="nav-link" exact>Dashboard</router-link>
      <router-link to="/alerts" class="nav-link">Alerts</router-link>
      <router-link to="/analytics" class="nav-link">Analytics</router-link>
      <router-link to="/settings" class="nav-link">Settings</router-link>
    </div>
    <div class="user-actions">
      <button class="btn btn-icon" title="Notifications" @click="goToAlerts">
        <i class="fas fa-bell" :class="{ 'has-notifications': hasUnreadNotifications }"></i>
        <span v-if="unreadCount > 0" class="notification-badge">{{ unreadCount }}</span>
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
  name: 'AppNavbar',
  data() {
    return {
      hasUnreadNotifications: false,
      unreadCount: 0,
      notifications: []
    }
  },
  methods: {
  goToAlerts() {
    this.$router.push('/alerts');
  },
  checkForNewNotifications() {
    // Simulate new notifications every 30 seconds
    this.notificationInterval = setInterval(() => {
      const newNotification = {
        id: Date.now(),
        title: 'New Alert',
        message: 'This is a simulated alert notification.',
        timestamp: new Date(),
        read: false
      };
      
      this.notifications.push(newNotification);
      this.hasUnreadNotifications = true;
      this.unreadCount = this.notifications.filter(n => !n.read).length;
    }, 30000); // 30 seconds
  }
  },
  mounted() {
    this.checkForNewNotifications();
    
    // Add initial notification to test
    setTimeout(() => {
      const newNotification = {
        id: Date.now(),
        title: 'Welcome Alert',
        message: 'Welcome to the AI Insights Dashboard! This is your first alert.',
        timestamp: new Date(),
        read: false
      };
      
      this.notifications.push(newNotification);
      this.hasUnreadNotifications = true;
      this.unreadCount = 1;  
    }, 2000); // 2 seconds after mounting
  },
  beforeUnmount() {
    // Clear interval when component is destroyed
    clearInterval(this.notificationInterval);
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

.notification-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background-color: #E53E3E;
  color: white;
  font-size: 0.7rem;
  min-width: 1.2rem;
  height: 1.2rem;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 0.25rem;
  font-weight: bold;
}

.btn-icon {
  position: relative;
}

.has-notifications {
  color: #3366CC !important; /* Dark blue color for notifications */
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
  100% {
    opacity: 1;
  }
}
</style>