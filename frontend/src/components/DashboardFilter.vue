// components/DashboardFilter.vue
<template>
  <div class="dashboard-filter">
    <div class="filter-section">
      <label for="date-range" class="filter-label">Time Range:</label>
      <select id="date-range" v-model="selectedDateRange" class="filter-select" @change="applyFilters">
        <option v-for="option in dateRangeOptions" :key="option.value" :value="option.value">
          {{ option.label }}
        </option>
      </select>
    </div>
    
    <div class="filter-section">
      <label for="team-filter" class="filter-label">Team:</label>
      <select id="team-filter" v-model="selectedTeam" class="filter-select" @change="applyFilters">
        <option value="all">All Teams</option>
        <option v-for="team in teamOptions" :key="team" :value="team">
          {{ team }}
        </option>
      </select>
    </div>
    
    <div class="filter-section">
      <button class="filter-refresh-btn" @click="$emit('refresh')">
        <i class="fas fa-sync-alt"></i>
        <span>Refresh Data</span>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardFilter',
  data() {
    return {
      selectedDateRange: 'day',
      selectedTeam: 'all',
      dateRangeOptions: [
        { label: 'Last 24 hours', value: 'day' },
        { label: 'Last 7 days', value: 'week' },
        { label: 'Last 30 days', value: 'month' },
        { label: 'Last quarter', value: 'quarter' },
        { label: 'Last year', value: 'year' },
        { label: 'Custom range', value: 'custom' }
      ],
      teamOptions: ['Marketing', 'Sales', 'Support', 'Development', 'Leadership']
    };
  },
  methods: {
    applyFilters() {
      this.$emit('filter-changed', {
        dateRange: this.selectedDateRange,
        team: this.selectedTeam
      });
    }
  }
}
</script>

<style scoped>
.dashboard-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.5rem;
  background-color: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px var(--shadow);
}

.filter-section {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-label {
  font-size: 0.875rem;
  color: var(--text);
  font-weight: 500;
}

.filter-select {
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid var(--secondary);
  background-color: white;
  color: var(--text);
  font-size: 0.875rem;
  min-width: 150px;
}

.filter-refresh-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: white;
  border: 1px solid var(--secondary);
  border-radius: 6px;
  color: var(--text);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-refresh-btn:hover {
  background-color: var(--primary);
  border-color: var(--primary);
  color: white;
}

@media (max-width: 768px) {
  .dashboard-filter {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-section {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .filter-select {
    width: 100%;
  }
}
</style>
