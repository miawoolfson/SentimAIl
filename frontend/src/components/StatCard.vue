// components/StatCard.vue
<template>
  <dashboard-card :title="title" :loading="loading" :refreshable="refreshable" @refresh="$emit('refresh')">
    <div class="stat-content">
      <div class="stat-value">{{ value }}</div>
      <div v-if="previousValue" class="stat-comparison" :class="comparisonClass">
        <i :class="comparisonIcon"></i>
        <span>{{ comparisonText }}</span>
      </div>
      <div class="stat-description">{{ description }}</div>
    </div>
  </dashboard-card>
</template>

<script>
import DashboardCard from './DashboardCard.vue';

export default {
  name: 'StatCard',
  components: {
    DashboardCard
  },
  props: {
    title: {
      type: String,
      required: true
    },
    value: {
      type: [String, Number],
      required: true
    },
    description: {
      type: String,
      default: ''
    },
    previousValue: {
      type: [String, Number],
      default: null
    },
    trend: {
      type: String,
      default: 'neutral',
      validator: (value) => ['up', 'down', 'neutral'].includes(value)
    },
    loading: {
      type: Boolean,
      default: false
    },
    refreshable: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    comparisonClass() {
      return {
        'trend-up': this.trend === 'up',
        'trend-down': this.trend === 'down',
        'trend-neutral': this.trend === 'neutral'
      };
    },
    comparisonIcon() {
      return {
        'up': 'fas fa-arrow-up',
        'down': 'fas fa-arrow-down',
        'neutral': 'fas fa-minus'
      }[this.trend];
    },
    comparisonText() {
      if (!this.previousValue) return '';
      
      const diff = parseFloat(this.value) - parseFloat(this.previousValue);
      const pct = (diff / parseFloat(this.previousValue) * 100).toFixed(1);
      
      if (isNaN(diff) || isNaN(pct)) return '';
      
      return `${diff > 0 ? '+' : ''}${pct}% from previous`;
    }
  }
}
</script>

<style scoped>
.stat-content {
  text-align: center;
  padding: 0.5rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 0.5rem;
}

.stat-comparison {
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
}

.trend-up {
  color: #38a169;
}

.trend-down {
  color: #e53e3e;
}

.trend-neutral {
  color: var(--secondary);
}

.stat-description {
  font-size: 0.875rem;
  color: var(--secondary);
}
</style>
