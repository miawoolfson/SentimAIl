const mailsService = require('../services/mails.service');

async function getAllMails(req, res, next) {
    try {
        res.json(await mailsService.getAllMails());
    } catch (err) {
        console.error(`Error while getting mails`, err.message);
        next(err);
    }
}


module.exports = {
    getAllMails,
};