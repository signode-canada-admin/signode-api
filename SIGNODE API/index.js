const express = require('express');
const cors = require('cors');

const db = require('./db');
const routes = require('./routes');

const app = express()
const apiport = 4000

app.use(cors())

db.on('error', console.error.bind(console, 'Mongo connection error'));

//test
app.get('/', (req, res)=>{
    res.send("SIGNODE API");    
})

app.use('/api', routes);

app.listen(apiport, (err)=>{
    console.log('api at port 4000');
})