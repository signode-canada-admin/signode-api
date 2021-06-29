const mongoose = require('mongoose')
const Schema = mongoose.Schema

const vars = new Schema(
    {
        _id: { type: String },
        temp_path: { type: String },
        email_archive: { type: String },
        code_path: { type: String },
        database: { type: String },
    }, 
    { 
        collection: 'vars' 
    }
)

const via = new Schema(
    {
        _id: {type: String},
        Signode_Ship_Via: [{type: String}]
    },
    {
        collection: 'via'
    }
)

const collectMar = new Schema(
    {
        "_id": { type: String },
        "dateReceived": { type: Date },
        "originalPrint": { type: Boolean },
        "emailAttachment": { type: String },
        "shipTo": { type: String },
        "via": { type: String },
        "PO": { type: String },
        "fileDirectory": { type: String },
        "status": { type: String },
        "shippedDate": { type: Date },
        "invoicedDate": { type: Date },
        "month": { type: String },
        "easyName": { type: String },
    },
    {
        collection: 'markham'
    }
)


module.exports = {
    vars: mongoose.model('vars', vars),
    via: mongoose.model('via', via), 
    collectMar: mongoose.model('collectMar', collectMar),
}


