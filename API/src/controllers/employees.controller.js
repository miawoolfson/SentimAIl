const employeesService = require('../services/employees.service');

async function getScores(req, res, next) {
    try {
        res.json(await employeesService.getScores());
    } catch (err) {
        console.error(`Error while getting employees scores`, err.message);
        next(err);
    }
}


module.exports = {
    getScores,
};