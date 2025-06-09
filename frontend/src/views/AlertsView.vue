<template>
  <div class="alerts-container">
    <h1 class="page-title">System Alerts</h1>
    
    <div class="alerts-list">
      <div v-if="notifications.length === 0" class="empty-state">
        <i class="fas fa-bell-slash"></i>
        <p>No alerts to display</p>
      </div>
      
      <div 
        v-for="notification in notifications" 
        :key="notification.id" 
        class="alert-item"
        :class="{ 'unread': !notification.read }"
      >
        <div class="alert-icon">
          <i class="fas fa-bell"></i>
        </div>
        <div class="alert-content">
          <h3 class="alert-title">{{ notification.title }}</h3>
          <p class="alert-message">{{ notification.message }}</p>
          <span class="alert-time">{{ formatTime(notification.timestamp) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AlertsView',
  data() {
    return {
      notifications: []
    }
  },
  methods: {
    formatTime(timestamp) {
      if (!timestamp) return '';
      
      const now = new Date();
      const time = new Date(timestamp);
      const diffMs = now - time;
      const diffSec = Math.floor(diffMs / 1000);
      
      if (diffSec < 60) return 'just now';
      if (diffSec < 3600) return `${Math.floor(diffSec / 60)}m ago`;
      if (diffSec < 86400) return `${Math.floor(diffSec / 3600)}h ago`;
      
      return time.toLocaleDateString();
    }
  },
  mounted() {
    // Add a couple of test notifications
    this.notifications.push({
      id: 1,
      title: 'System Alert',
      message: 'This is a test alert notification.',
      timestamp: new Date(),
      read: false
    });
    
    this.notifications.push({
      id: 2,
      title: 'Email Sentiment Alert',
      message: 'Negative sentiment detected in recent communications.',
      timestamp: new Date(Date.now() - 1000 * 60 * 30), // 30 minutes ago
      read: true
    });
  }
}
</script>

<style scoped>
.alerts-container {
  max-width: 800px;
  margin: 0 auto;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 1.5rem;
}

.alerts-list {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.empty-state {
  padding: 3rem 1rem;
  text-align: center;
  color: #7F8FA6;
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.alert-item {
  display: flex;
  padding: 1rem;
  border-bottom: 1px solid rgba(0,0,0,0.05);
}

.alert-item:last-child {
  border-bottom: none;
}

.alert-item.unread {
  background-color: rgba(51, 102, 204, 0.05);
}

.alert-icon {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background-color: rgba(51, 102, 204, 0.1);
  color: #3366CC;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  flex-shrink: 0;
}

.alert-content {
  flex: 1;
}

.alert-title {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 0.25rem 0;
}

.alert-message {
  color: #7F8FA6;
  margin: 0 0 0.5rem 0;
}

.alert-time {
  font-size: 0.75rem;
  color: #7F8FA6;
}
</style>