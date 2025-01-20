const express = require('express');
const router = express.Router();
const employeesController = require('../controllers/employees.controller');

router.get('/scores', employeesController.getScores);

module.exports = router;