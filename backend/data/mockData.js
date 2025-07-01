// data/mockData.js
const now = new Date();

module.exports = {
  // Dashboard stats
  dashboardStats: {
    totalCommunications: 1284,
    previousCommunications: 1156,
    communicationsTrend: 'up',
    avgResponseTime: 74,
    previousResponseTime: 82,
    responseTrend: 'up',
    communicationScore: 8.4,
    previousScore: 8.2,
    scoreTrend: 'up',
    actionItems: 23,
    previousActionItems: 27,
    actionItemsTrend: 'down'
  },
  
  // Communications
  communications: [
    {
      id: 'comm-1',
      type: 'email',
      sender: 'John Doe (Acme Corp)',
      subject: 'Quarterly Business Review',
      preview: "Looking forward to our meeting next week. I've prepared the documents you requested.",
      timestamp: new Date(now.getTime() - 1000 * 60 * 30),
      tags: ['client', 'meeting', 'follow-up']
    },
    {
      id: 'comm-2',
      type: 'email',
      sender: 'Sarah Johnson (Marketing)',
      subject: 'Updated Marketing Materials',
      preview: "Here are the updated brochures for the new product line.",
      timestamp: new Date(now.getTime() - 1000 * 60 * 120),
      tags: ['internal', 'marketing']
    }
  ],
  
  // Recommendations
  recommendations: [
    {
      id: 'rec-1',
      priority: 'high',
      title: 'Respond to Acme Corp RFP',
      description: 'The deadline for the Acme Corp RFP is approaching in 48 hours.',
      teams: ['sales', 'leadership']
    }
  ],
  
  // Teams
  teams: [
    { id: 'sales', name: 'Sales', color: '#4299E1' },
    { id: 'marketing', name: 'Marketing', color: '#ED8936' }
  ],
  
  // Current user
  currentUser: {
    id: 'user-1',
    name: 'Robert Taylor',
    email: 'robert@example.com',
    role: 'CEO'
  },
  
  // Notifications
  notifications: [
    {
      id: 'notif-1',
      type: 'info',
      message: 'Weekly analytics report available',
      time: new Date(now.getTime() - 1000 * 60 * 30),
      read: false
    }
  ]
};