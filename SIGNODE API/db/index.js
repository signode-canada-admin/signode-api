const mongoose = require('mongoose');

const DB = 'signode';

mongoose
    .connect(`mongodb://127.0.0.1:27017/${DB}`, { useNewUrlParser: true, useUnifiedTopology: true })
    .catch( e => {
        console.error('db connection error', e.message)
    })

const db = mongoose.connection

module.exports = db