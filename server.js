// server.js

var express = require('express');
var path = require('path');
var fs = require('fs');
var serveStatic = require('serve-static');

app = express();
app.use(serveStatic(__dirname + "/web/sobrecupo-web/dist"));

var port = process.env.PORT || 5000;
app.listen(port);

console.log('server started: '+ port);


app.get('/salones', (request, response) => {
    fs.readFile('classrooms.json', 'utf8', (error, data) => {
        if(error){
            console.error(error);
        }
        response.send(data);
    })
});