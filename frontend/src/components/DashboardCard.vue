<template>
  <div class="dashboard-card" :class="{ 'is-loading': loading }">
    <div class="card-header">
      <h3 class="card-title">{{ title }}</h3>
      <div class="card-actions">
        <button v-if="refreshable" class="card-refresh-btn" @click="$emit('refresh')" :disabled="loading">
          <i class="fas fa-sync-alt" :class="{ 'fa-spin': loading }"></i>
        </button>
        <slot name="actions"></slot>
      </div>
    </div>
    <div class="card-content">
      <div v-if="loading" class="card-loader">
        <div class="card-spinner"></div>
      </div>
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardCard',
  props: {
    title: {
      type: String,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    },
    refreshable: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.dashboard-card {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px var(--shadow);
  overflow: hidden;
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: box-shadow 0.3s;
}

.dashboard-card:hover {
  box-shadow: 0 4px 12px var(--shadow);
}

.card-header {
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(0,0,0,0.05);
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text);
  margin: 0;
}

.card-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.card-refresh-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--secondary);
  font-size: 0.875rem;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s;
}

.card-refresh-btn:hover {
  color: var(--primary);
  background-color: rgba(0,0,0,0.05);
}

.card-refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.card-content {
  padding: 1rem;
  flex: 1;
  position: relative;
}

.card-loader {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255,255,255,0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 5;
}

.card-spinner {
  width: 30px;
  height: 30px;
  border: 3px solid var(--secondary);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.is-loading .card-content {
  min-height: 100px;
}
</style>