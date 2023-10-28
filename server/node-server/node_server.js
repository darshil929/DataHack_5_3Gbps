const express = require('express')
const request = require('request');

app = express();
const PORT = 3000;

app.get('/home', function (req, res) {
    request('http://127.0.0.1:5000/flask', function (error, response, body) {
        console.error('error:', error); // error printing
        console.log('statusCode:', response && response.statusCode); // if response received -> print response status code 
        console.log('body:', body); // recieved data printing
        res.send(body); // display response on website
    });
});

app.listen(PORT, function () {
    console.log('Listening on Port 3000');
});