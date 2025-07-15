// src/services/superSimpleService.js
import axios from 'axios';

class SuperSimpleService {
  constructor() {
    this.seenIds = new Set();
    this.isRunning = false;
    this.notifications = [];
    this.loadNotifications();
  }

  loadNotifications() {
    try {
      const saved = localStorage.getItem('sentiment_notifications');
      if (saved) {
        this.notifications = JSON.parse(saved);
        // Rebuild seenIds from saved notifications
        this.notifications.forEach(notification => {
          if (notification.data && notification.data.id) {
            this.seenIds.add(notification.data.id);
          }
        });
      }
    } catch (error) {
      console.error('Failed to load notifications:', error);
    }
  }

  saveNotifications() {
    try {
      console.log('💾 Saving notifications to localStorage:', this.notifications.length);
      localStorage.setItem('sentiment_notifications', JSON.stringify(this.notifications));
      window.globalNotifications = this.notifications;
      console.log('✅ Successfully saved to localStorage and window.globalNotifications');
    } catch (error) {
      console.error('❌ Failed to save notifications:', error);
    }
  }

  async checkAndAlert() {
    try {
      console.log('🔍 Checking for negative sentiment...');
      
      const response = await axios.get('/api/negative-sentiment');
      console.log('📊 Response:', response.data);
      
      if (response.data && response.data.length > 0) {
        response.data.forEach(email => {
          if (!this.seenIds.has(email.id)) {
            // New email found - show popup AND save to localStorage
            this.showPopup(email);
            this.saveNotification(email);
            this.seenIds.add(email.id);
          }
        });
      }
    } catch (error) {
      console.error('❌ Error:', error);
    }
  }

  saveNotification(email) {
    const notification = {
      id: `sentiment_${email.id}_${Date.now()}`,
      type: 'warning',
      title: 'Negative Sentiment Alert',
      message: `"${email.subject}" from ${email.sender}`,
      timestamp: new Date(),
      read: false,
      data: email
    };

    this.notifications.push(notification);
    this.saveNotifications();
    
    console.log('💾 Saved notification to localStorage:', notification.id);
  }

  showPopup(email) {
    console.log('🚨 SHOWING POPUP for email:', email.id);
    
    // Simple alert popup
    alert(`🚨 NEGATIVE SENTIMENT ALERT!\n\nSubject: ${email.subject}\nFrom: ${email.sender}\nTime: ${email.insert_time}`);
    
    // Also try browser notification with custom title
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification('🚨 Sentimail Alert', {
        body: `Negative sentiment: "${email.subject}" from ${email.sender}`,
        icon: '/favicon.svg', // Use your new brain icon
        badge: '/favicon.svg',
        tag: 'sentiment-alert', // Prevents duplicate notifications
        requireInteraction: false,
        silent: false
      });
    }
  }

  start() {
    if (this.isRunning) return;
    
    console.log('🚀 Starting simple monitoring...');
    this.isRunning = true;
    
    // Check immediately
    this.checkAndAlert();
    
    // Check every 15 seconds
    setInterval(() => {
      this.checkAndAlert();
    }, 15000);
    
    // Request notification permission
    if ('Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission();
    }
  }

  stop() {
    this.isRunning = false;
  }
}

const simpleService = new SuperSimpleService();
export default simpleService;