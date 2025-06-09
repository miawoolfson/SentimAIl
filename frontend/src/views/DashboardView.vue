<template>
    <div>
      <h1 class="dashboard-title">Management Insights Dashboard</h1>
      
      <div class="dashboard-container">
        <div class="loading-overlay" v-if="isLoading">
          <div class="loading-spinner"></div>
        </div>
        <iframe 
          :src="grafanaUrl" 
          class="grafana-iframe" 
          @load="handleIframeLoad"
          allowfullscreen>
        </iframe>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'DashboardView',
    data() {
      return {  
        isLoading: true,
        grafanaUrl: 'http://sentimail.cs.colman.ac.il:3000/public-dashboards/16a10e29762c4af9ace225811bc12c75'
    }
    },
    methods: {
      handleIframeLoad() {
        this.isLoading = false;
      }
    },
    mounted() {
      // Set a fallback timer to hide loading state if iframe load event fails
      setTimeout(() => {
        this.isLoading = false;
      }, 5000);
    }
  }
  </script>
  
  <style scoped>
  .dashboard-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 1.5rem;
  }
  
  .dashboard-container {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 6px var(--shadow);
    overflow: hidden;
    height: 500px;
    position: relative;
    margin-bottom: 1rem;
  }
  
  .loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
}

  .loading-spinner {
    width: 50px;
    height: 50px;
    border: 5px solid #7F8FA6;
    border-top-color: #3366CC;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
  
  .grafana-iframe {
    width: 100%;
    height: 100%;
    border: none;
  }
  .dashboard-info {
  background-color: #f0f4f8;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

  </style>