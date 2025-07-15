<template>
  <div class="alerts-container">
    <h1 class="page-title">System Alerts</h1>
    
    <div class="alerts-list">
      <div v-if="recentNotifications.length === 0" class="empty-state">
        <i class="fas fa-bell-slash"></i>
        <p>No recent alerts to display</p>
        <small>Showing alerts from the past 2 days</small>
      </div>
      
      <div 
        v-for="notification in recentNotifications" 
        :key="notification.id" 
        class="alert-item"
        :class="{ 'unread': !notification.read }"
        @click="markAsRead(notification.id)"
      >
        <div class="alert-icon">
          <i class="fas fa-exclamation-triangle" v-if="notification.type === 'warning'"></i>
          <i class="fas fa-info-circle" v-else></i>
        </div>
        <div class="alert-content">
          <h3 class="alert-title">{{ notification.title }}</h3>
          <p class="alert-message">{{ notification.message }}</p>
          <span class="alert-time">{{ formatTime(notification.timestamp) }}</span>
          <div v-if="notification.data" class="alert-details">
            <small><strong>Email ID:</strong> {{ notification.data.id }}</small>
            <small><strong>Created:</strong> {{ formatTime(notification.data.created_at) }}</small>
          </div>
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
  computed: {
    recentNotifications() {
      // Filter notifications from the past 2 days
      const twoDaysAgo = new Date(Date.now() - 2 * 24 * 60 * 60 * 1000);
      
      return this.notifications.filter(notification => {
        const notificationDate = new Date(notification.timestamp);
        return notificationDate >= twoDaysAgo;
      }).sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)); // Sort newest first
    }
  },
  methods: {
    loadNotifications() {
      try {
        // Load from localStorage
        const saved = localStorage.getItem('sentiment_notifications');
        console.log('🔍 Raw localStorage data:', saved);
        
        if (saved) {
          this.notifications = JSON.parse(saved);
          console.log('📦 Parsed notifications:', this.notifications);
        } else {
          console.log('❌ No saved notifications found in localStorage');
        }
        
        // Also check global notifications from Navbar
        if (window.globalNotifications) {
          console.log('🌐 Global notifications found:', window.globalNotifications);
          this.notifications = window.globalNotifications;
        } else {
          console.log('❌ No global notifications found');
        }
        
        console.log(`📊 Final notifications count: ${this.notifications.length}`);
        console.log(`📊 Recent notifications count: ${this.recentNotifications.length}`);
        
        // Clean up old notifications from storage (older than 7 days)
        this.cleanOldNotifications();
      } catch (error) {
        console.error('Failed to load notifications in AlertsView:', error);
      }
    },
    
    cleanOldNotifications() {
      const sevenDaysAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
      const originalCount = this.notifications.length;
      
      this.notifications = this.notifications.filter(notification => {
        const notificationDate = new Date(notification.timestamp);
        return notificationDate >= sevenDaysAgo;
      });
      
      if (this.notifications.length < originalCount) {
        console.log(`🗑️ Cleaned ${originalCount - this.notifications.length} old notifications`);
        this.saveNotifications();
      }
    },
    
    markAsRead(notificationId) {
      const notification = this.notifications.find(n => n.id === notificationId);
      if (notification) {
        notification.read = true;
        this.saveNotifications();
      }
    },
    
    saveNotifications() {
      try {
        localStorage.setItem('sentiment_notifications', JSON.stringify(this.notifications));
        window.globalNotifications = this.notifications;
      } catch (error) {
        console.error('Failed to save notifications:', error);
      }
    },
    
    formatTime(timestamp) {
      if (!timestamp) return '';
      
      const now = new Date();
      const time = new Date(timestamp);
      const diffMs = now - time;
      const diffSec = Math.floor(diffMs / 1000);
      
      if (diffSec < 60) return 'just now';
      if (diffSec < 3600) return `${Math.floor(diffSec / 60)}m ago`;
      if (diffSec < 86400) return `${Math.floor(diffSec / 3600)}h ago`;
      if (diffSec < 172800) return 'yesterday';
      
      return time.toLocaleDateString();
    }
  },
  
  mounted() {
    console.log('📋 AlertsView mounted - loading recent notifications');
    this.loadNotifications();
    
    // Refresh notifications every 5 seconds to stay in sync
    setInterval(() => {
      console.log('🔄 AlertsView refreshing notifications...');
      this.loadNotifications();
    }, 5000);
  }
}
</script>

<style scoped>
.alerts-container {
  /* Remove max-width and center alignment to make it left-aligned like other pages */
  padding: 0;
  margin: 0;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 1.5rem;
  text-align: left; /* Ensure left alignment */
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

.empty-state small {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: #A0AEC0;
}

.alert-item {
  display: flex;
  padding: 1rem;
  border-bottom: 1px solid rgba(0,0,0,0.05);
  cursor: pointer;
  transition: background-color 0.2s;
}

.alert-item:hover {
  background-color: rgba(0,0,0,0.02);
}

.alert-item:last-child {
  border-bottom: none;
}

.alert-item.unread {
  background-color: rgba(51, 102, 204, 0.05);
  border-left: 4px solid var(--primary);
}

.alert-icon {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background-color: rgba(229, 62, 62, 0.1);
  color: #E53E3E;
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

.alert-details {
  margin-top: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.alert-details small {
  color: #7F8FA6;
  font-size: 0.7rem;
}
</style>