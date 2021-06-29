const express = require('express');

const db = require('./db');
const routes = require('./routes');

const app = express()
const apiport = 4000

db.on('error', console.error.bind(console, 'Mongo connection error'));

//test
app.get('/', (req, res)=>{
    res.send("PASS");
})

app.use('/api', routes);

app.listen(apiport, (err)=>{
    console.log('api at port 4000');
})