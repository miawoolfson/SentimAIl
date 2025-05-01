// routes/api.js
const express = require('express');
const router = express.Router();

// Mock data - In a real application, this would come from a database
const mockData = require('../data/mockData');

// Dashboard stats
router.get('/dashboard/stats', (req, res) => {
  // Process filters from query params if needed
  const { dateRange, team } = req.query;
  
  // Simulate processing based on filters
  let stats = { ...mockData.dashboardStats };
  
  // Return data
  setTimeout(() => {
    res.json({ success: true, data: stats });
  }, 500); // Simulate network delay
});

// Recent communications
router.get('/communications/recent', (req, res) => {
  const { dateRange, team, limit = 10 } = req.query;
  
  // Filter communications based on params
  let communications = [...mockData.communications];
  
  if (team && team !== 'all') {
    communications = communications.filter(comm => 
      comm.tags.includes(team.toLowerCase()) || 
      comm.sender.toLowerCase().includes(team.toLowerCase())
    );
  }
  
  // Limit results
  communications = communications.slice(0, parseInt(limit));
  
  setTimeout(() => {
    res.json({ success: true, data: communications });
  }, 600);
});

// Recommendations
router.get('/recommendations', (req, res) => {
  const { dateRange, team } = req.query;
  
  // Filter recommendations based on params
  let recommendations = [...mockData.recommendations];
  
  if (team && team !== 'all') {
    recommendations = recommendations.filter(rec => 
      rec.teams.includes(team)
    );
  }
  
  setTimeout(() => {
    res.json({ success: true, data: recommendations });
  }, 700);
});

// Teams
router.get('/teams', (req, res) => {
  setTimeout(() => {
    res.json({ success: true, data: mockData.teams });
  }, 300);
});

router.get('/teams/:id/members', (req, res) => {
  const teamId = req.params.id;
  const team = mockData.teams.find(t => t.id === teamId);
  
  if (!team) {
    return res.status(404).json({ success: false, message: 'Team not found' });
  }
  
  const members = mockData.teamMembers.filter(m => m.teamId === teamId);
  
  setTimeout(() => {
    res.json({ success: true, data: members });
  }, 400);
});

// User profile
router.get('/user/profile', (req, res) => {
  // In a real app, this would use authentication to get the current user
  setTimeout(() => {
    res.json({ success: true, data: mockData.currentUser });
  }, 200);
});

router.post('/user/settings', (req, res) => {
  const settings = req.body;
  
  // In a real app, this would update the user's settings in the database
  setTimeout(() => {
    res.json({ success: true, message: 'Settings updated successfully' });
  }, 300);
});

// Notifications
router.get('/notifications', (req, res) => {
  setTimeout(() => {
    res.json({ success: true, data: mockData.notifications });
  }, 300);
});

router.post('/notifications/:id/read', (req, res) => {
  const notificationId = req.params.id;
  
  // In a real app, this would mark the notification as read in the database
  setTimeout(() => {
    res.json({ success: true, message: 'Notification marked as read' });
  }, 200);
});

router.post('/notifications/read-all', (req, res) => {
  // In a real app, this would mark all notifications as read in the database
  setTimeout(() => {
    res.json({ success: true, message: 'All notifications marked as read' });
  }, 300);
});

// Analytics
router.get('/analytics/:metric', (req, res) => {
  const metric = req.params.metric;
  const { dateRange, team } = req.query;
  
  let data = null;
  
  switch (metric) {
    case 'communication-volume':
      data = mockData.analytics.communicationVolume;
      break;
    case 'response-times':
      data = mockData.analytics.responseTimes;
      break;
    case 'sentiment-analysis':
      data = mockData.analytics.sentimentAnalysis;
      break;
    default:
      return res.status(404).json({ success: false, message: 'Metric not found' });
  }
  
  setTimeout(() => {
    res.json({ success: true, data });
  }, 800);
});

// Reports
router.get('/reports', (req, res) => {
  const { dateRange, team } = req.query;
  
  let reports = [...mockData.reports];
  
  if (team && team !== 'all') {
    reports = reports.filter(report => report.team === team);
  }
  
  setTimeout(() => {
    res.json({ success: true, data: reports });
  }, 500);
});

router.get('/reports/:id', (req, res) => {
  const reportId = req.params.id;
  const report = mockData.reports.find(r => r.id === reportId);
  
  if (!report) {
    return res.status(404).json({ success: false, message: 'Report not found' });
  }
  
  setTimeout(() => {
    res.json({ success: true, data: report });
  }, 600);
});

router.post('/reports/generate', (req, res) => {
  const params = req.body;
  
  // In a real app, this would generate a new report based on parameters
  setTimeout(() => {
    res.json({ 
      success: true, 
      message: 'Report generation started',
      data: {
        id: 'new-report-' + Date.now(),
        status: 'processing',
        estimatedCompletion: new Date(Date.now() + 30000) // 30 seconds from now
      }
    });
  }, 1000);
});

module.exports = router;