var fs = require('fs');
const db = require('./db.service');

const path = './src/services/SQL/mails/'

async function getAllMails() {
    var sql = fs.readFileSync(path + 'all.sql').toString();
    const rows = await db.select(sql, []);
    return {
        rows
    }
}

module.exports = {
    getAllMails,
}