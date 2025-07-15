//http://localhost:5000/api/negative-sentiment
// server.js
require('dotenv').config(); // Load environment variables

const express = require('express');
const cors = require('cors');
const { Client } = require('pg');

const app = express();
app.use(cors());
app.use(express.json());

// YOUR DATABASE INFO
const dbConfig = {
  host: process.env.DB_HOST || 'localhost',
  port: process.env.DB_PORT || 5432,
  database: process.env.DB_NAME || 'postgres',
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD, // This will come from .env file
  ssl: {
    rejectUnauthorized: false
  }
};

// Validate required environment variables
if (!process.env.DB_PASSWORD) {
  console.error('❌ ERROR: DB_PASSWORD environment variable is required');
  process.exit(1);
}

console.log('🔧 Database config:', {
  host: dbConfig.host,
  port: dbConfig.port,
  database: dbConfig.database,
  user: dbConfig.user,
  password: '***hidden***'
});

app.get('/api/negative-sentiment', async (req, res) => {
  console.log('🔍 API called - checking database...');
  try {
    const { since } = req.query;
    
    console.log('📡 Connecting to database:', dbConfig.host, dbConfig.database);
    const client = new Client(dbConfig);
    await client.connect();
    console.log('✅ Database connected successfully');
    
    const query = `
      SELECT id, subject, sender, sentiment_tag, created_at
      FROM public.emails_etl
      WHERE sentiment_tag = 'negative'
      AND created_at > NOW() - INTERVAL '15 seconds'
      ORDER BY created_at DESC
      LIMIT 10
    `;
    
    console.log('🔎 Running query for last 15 seconds:', query);
    const result = await client.query(query);
    console.log(`📊 Query result: Found ${result.rows.length} rows`);
    
    await client.end();
    res.json(result.rows);
  } catch (error) {
    console.error('💥 Database error:', error.message);
    console.error('🔧 Error details:', error);
    res.status(500).json({ error: error.message });
  }
});

app.listen(5000, () => {
  console.log('Backend running on http://localhost:5000');
});