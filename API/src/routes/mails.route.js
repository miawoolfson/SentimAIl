const express = require('express');
const router = express.Router();
const mailsController = require('../controllers/mails.controller');

router.get('/', mailsController.getAllMails);

module.exports = router;