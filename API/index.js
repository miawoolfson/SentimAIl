const express = require('express');
const bodyParser = require('body-parser');
var cors = require('cors');
const dotenv = require('dotenv');
dotenv.config();

const mailsRouter = require('./src/routes/mails.route');
const employeesRouter = require('./src/routes/employees.route');

const app = express();
const port = process.env.PORT;

app.use(express.json());

app.use(cors())
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.use('/mails', mailsRouter);
app.use('/employees', employeesRouter);

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
