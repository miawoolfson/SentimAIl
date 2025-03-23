var fs = require('fs');
const db = require('./db.service');

const path = './src/services/SQL/Employees/'

async function getScores() {
    var sql = fs.readFileSync(path + 'scores.sql').toString();
    const rows = await db.select(sql, []);
    return {
        rows
    }
}

module.exports = {
    getScores,
}