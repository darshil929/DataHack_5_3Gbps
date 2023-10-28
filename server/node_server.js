const express = require('express');
const request = require('request');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();

const db = require('./Utils/database');

require('dotenv').config();

const PORT = process.env.PORT || 3000;

app.use(cors());

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());


app.get('/get-data', (req, res) => {
    request('http://127.0.0.1:5000/test-get', (error, response, body) => {
        if (!error && response.statusCode === 200) {
            const data = JSON.parse(body);
            res.status(200).json(data);
        } else {
            res.status(500).json({ error: 'Error fetching data from Flask' });
        }
    });
});

app.post('/send-data', (req, res) => {

    request.post('http://127.0.0.1:5000/test-post', {
        json: req.body,
    }, (error, response, body) => {
        if (!error && response.statusCode === 200) {
            res.status(200).json({ message: 'Data sent to Flask!' });
        } else {
            res.status(500).json({ error: 'Error sending data to Flask' });
        }
    });
});

db.mongoConnect(() => {

    app.listen(PORT, () => {
        console.log(`Server is running at port ${PORT}...`);
    });

});