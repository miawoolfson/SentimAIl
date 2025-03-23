const { Pool } = require('pg');

const pool = new Pool({
    user: process.env.DB_USER,
    host: process.env.DB_HOST,
    database: process.env.DB_NAME,
    password: process.env.DB_PASSWORD,
    port: process.env.DB_PORT,
    pgbouncer: true
});

async function select(sql, params) {
    const query = {
        name: (sql + params).slice(-60),
        text: sql,
        values: params,
    }
    return new Promise((resolve, reject) => {
        pool.query(
            query,
            (error, results) => {
                if (error) {
                    reject(error);
                }
                try {
                    resolve(results.rows);
                } catch (e) {
                    console.log(e)
                }
            }
        );
    });
}

async function insertOne(sql, params) {
    const query = {
        name: (sql + params).slice(-60),
        text: sql,
        values: params,
    }
    return new Promise((resolve, reject) => {
        pool.query(
            query,
            (error, results) => {
                if (error) {
                    reject(error);
                }
                try {
                    resolve(results.rows[0].id);
                } catch (e) {
                    console.log(e)
                }
            }
        );
    });
}

async function update(sql, params) {
    const query = {
        name: (sql + params).slice(-60),
        text: sql,
        values: params,
    }
    return new Promise((resolve, reject) => {
        pool.query(
            query,
            (error, results) => {
                if (error) {
                    reject(error);
                }
                try {
                    resolve(results);
                } catch (e) {
                    console.log(e)
                }
            }
        );
    });
}

async function deleteOne(sql, params) {
    const query = {
        name: (sql + params).slice(-60),
        text: sql,
        values: params,
    }
    return new Promise((resolve, reject) => {
        pool.query(
            query,
            (error, results) => {
                if (error) {
                    reject(error);
                }
                try {
                    resolve(results);
                } catch (e) {
                    console.log(e)
                }
            }
        );
    });
}

module.exports = {
    select,
    insertOne,
    update,
    deleteOne
}