// components/NotificationTray.vue
<template>
  <div class="notification-tray">
    <button class="notification-toggle" @click="isOpen = !isOpen">
      <i class="fas fa-bell"></i>
      <span v-if="unreadCount > 0" class="notification-badge">{{ formattedCount }}</span>
    </button>
    
    <div class="notification-panel" v-if="isOpen" v-click-outside="close">
      <div class="notification-header">
        <h4 class="notification-title">Notifications</h4>
        <button v-if="notifications.length > 0" class="notification-action" @click="markAllRead">
          Mark all as read
        </button>
      </div>
      
      <div class="notification-list" v-if="notifications.length > 0">
        <div 
          v-for="notification in notifications" 
          :key="notification.id" 
          class="notification-item"
          :class="{ 'is-unread': !notification.read }"
          @click="markRead(notification.id)"
        >
          <div class="notification-icon" :class="`notification-${notification.type}`">
            <i :class="getIconForType(notification.type)"></i>
          </div>
          <div class="notification-content">
            <p class="notification-message">{{ notification.message }}</p>
            <span class="notification-time">{{ formatTime(notification.time) }}</span>
          </div>
        </div>
      </div>
      
      <div v-else class="notification-empty">
        <i class="fas fa-check-circle"></i>
        <p>You're all caught up!</p>
      </div>
      
      <div class="notification-footer">
        <button class="notification-settings">
          <i class="fas fa-cog"></i>
          <span>Notification settings</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotificationTray',
  props: {
    notifications: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      isOpen: false
    };
  },
  computed: {
    unreadCount() {
      return this.notifications.filter(n => !n.read).length;
    },
    formattedCount() {
      return this.unreadCount > 99 ? '99+' : this.unreadCount;
    }
  },
  methods: {
    close() {
      this.isOpen = false;
    },
    markRead(id) {
      this.$emit('mark-read', id);
    },
    markAllRead() {
      this.$emit('mark-all-read');
    },
    getIconForType(type) {
      const icons = {
        info: 'fas fa-info-circle',
        success: 'fas fa-check-circle',
        warning: 'fas fa-exclamation-triangle',
        error: 'fas fa-times-circle',
        update: 'fas fa-upload',
        message: 'fas fa-comment'
      };
      return icons[type] || icons.info;
    },
    formatTime(timestamp) {
      // Simple relative time formatter
      const now = new Date();
      const time = new Date(timestamp);
      const diff = Math.floor((now - time) / 1000); // seconds
      
      if (diff < 60) return 'just now';
      if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
      if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
      if (diff < 604800) return `${Math.floor(diff / 86400)}d ago`;
      
      return time.toLocaleDateString();
    }
  },
  directives: {
    clickOutside: {
      mounted(el, binding) {
        el.__click_outside_handler__ = (event) => {
          if (!(el === event.target || el.contains(event.target))) {
            binding.value(event);
          }
        };
        document.addEventListener('click', el.__click_outside_handler__);
      },
      unmounted(el) {
        document.removeEventListener('click', el.__click_outside_handler__);
      }
    }
  }
}
</script>

<style scoped>
.notification-tray {
  position: relative;
}

.notification-toggle {
  background: none;
  border: none;
  position: relative;
  cursor: pointer;
  padding: 0.5rem;
  font-size: 1.25rem;
  color: var(--text);
  transition: color 0.3s;
}

.notification-toggle:hover {
  color: var(--primary);
}

.notification-badge {
  position: absolute;
  top: 0;
  right: 0;
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

.notification-panel {
  position: absolute;
  top: 100%;
  right: 0;
  width: 320px;
  max-height: 80vh;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 100;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.notification-header {
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.notification-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.notification-action {
  background: none;
  border: none;
  font-size: 0.8rem;
  color: var(--primary);
  cursor: pointer;
}

.notification-list {
  flex: 1;
  overflow-y: auto;
  max-height: 350px;
}

.notification-item {
  display: flex;
  padding: 0.75rem 1rem;
  gap: 0.75rem;
  cursor: pointer;
  transition: background-color 0.2s;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.notification-item:hover {
  background-color: rgba(0, 0, 0, 0.02);
}

.notification-item.is-unread {
  background-color: rgba(51, 102, 204, 0.05);
}

.notification-icon {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.notification-info {
  background-color: rgba(51, 102, 204, 0.1);
  color: var(--primary);
}

.notification-success {
  background-color: rgba(56, 161, 105, 0.1);
  color: #38A169;
}

.notification-warning {
  background-color: rgba(236, 201, 75, 0.1);
  color: #ECC94B;
}

.notification-error {
  background-color: rgba(229, 62, 62, 0.1);
  color: #E53E3E;
}

.notification-update {
  background-color: rgba(128, 90, 213, 0.1);
  color: #805AD5;
}

.notification-message {
  background-color: rgba(45, 55, 72, 0.1);
  color: var(--text);
}

.notification-content {
  flex: 1;
}

.notification-message {
  margin: 0 0 0.25rem 0;
  font-size: 0.9rem;
}

.notification-time {
  font-size: 0.75rem;
  color: var(--secondary);
}

.notification-empty {
  padding: 2rem;
  text-align: center;
  color: var(--secondary);
}

.notification-empty i {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: #38A169;
}

.notification-empty p {
  margin: 0;
}

.notification-footer {
  padding: 0.75rem;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.notification-settings {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  background: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: var(--secondary);
  cursor: pointer;
  transition: all 0.2s;
}

.notification-settings:hover {
  background-color: rgba(0, 0, 0, 0.02);
  color: var(--primary);
}
</style>