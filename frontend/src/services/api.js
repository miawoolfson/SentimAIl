// src/services/api.js
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.VUE_APP_API_URL,
  withCredentials: false,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json'
  },
  timeout: 10000
});

export default {
  // Dashboard data
  getDashboardStats(filters = {}) {
    return apiClient.get('/dashboard/stats', { params: filters });
  },
  
  getRecentCommunications(filters = {}) {
    return apiClient.get('/communications/recent', { params: filters });
  },
  
  getRecommendations(filters = {}) {
    return apiClient.get('/recommendations', { params: filters });
  },
  
  // Team data
  getTeams() {
    return apiClient.get('/teams');
  },
  
  getTeamMembers(teamId) {
    return apiClient.get(`/teams/${teamId}/members`);
  },
  
  // User data
  getUserProfile() {
    return apiClient.get('/user/profile');
  },
  
  updateUserSettings(settings) {
    return apiClient.post('/user/settings', settings);
  },
  
  // Notifications
  getNotifications() {
    return apiClient.get('/notifications');
  },
  
  markNotificationRead(id) {
    return apiClient.post(`/notifications/${id}/read`);
  },
  
  markAllNotificationsRead() {
    return apiClient.post('/notifications/read-all');
  },
  
  // Analytics
  getAnalyticsData(metric, filters = {}) {
    return apiClient.get(`/analytics/${metric}`, { params: filters });
  },
  
  // Reports
  getReports(filters = {}) {
    return apiClient.get('/reports', { params: filters });
  },
  
  getReportById(id) {
    return apiClient.get(`/reports/${id}`);
  },
  
  generateReport(params) {
    return apiClient.post('/reports/generate', params);
  },
  
  // Grafana helper
  getGrafanaUrl(dashboard, timeRange = {}) {
    const baseUrl = process.env.VUE_APP_GRAFANA_URL;
    const from = timeRange.from || 'now-24h';
    const to = timeRange.to || 'now';
    return `${baseUrl}/d/${dashboard}/${dashboard}?orgId=1&from=${from}&to=${to}`;
  }
};