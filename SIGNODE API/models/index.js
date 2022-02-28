const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const vars = new Schema(
  {
    _id: { type: String },
    temp_path: { type: String },
    email_archive: { type: String },
    code_path: { type: String },
    database: { type: String },
  },
  {
    collection: "vars",
  }
);

const via = new Schema(
  {
    _id: { type: String },
    Signode_Ship_Via: [{ type: String }],
  },
  {
    collection: "via",
  }
);

const partsQRSchema = new Schema(
  {
    _id: { type: Number },
    body: { type: String },
  },
  {
    collection: "partsQR",
  }
);

const tickectsSchema = {
  _id: { type: String },
  dateReceived: { type: Date },
  originalPrint: { type: Boolean },
  emailAttachment: { type: String },
  shipTo: { type: String },
  via: { type: String },
  PO: { type: String },
  fileDirectory: { type: String },
  status: { type: String },
  shippedDate: { type: Date },
  invoicedDate: { type: Date },
  month: { type: String },
  easyName: { type: String },
};

const collectMar = new Schema(tickectsSchema, {
  collection: "markham",
});

const collectSurr = new Schema(tickectsSchema, {
  collection: "surrey",
});

const collectGlen = new Schema(tickectsSchema, {
  collection: "glenview",
});

const siteNames = new Schema(
  {
    _id: { type: String },
    list: [{ type: String }],
  },
  {
    collection: "siteList",
  }
);

const ediMetaData = new Schema(
  {
    _id: { type: String },
    data: {
        customer_name: {type: Number},
        ship_to: {type: String},
        warehouse: {type: String},
        order_type: {type: String}
    }
  }, 
  {
    collection: "ediMetaData"
  }
)


const bunzlCrossRef = new Schema(
  {
    _id: {type: String},
    customer: {type: Number},
    name: {type: String},
    sig_prod: {type: String},
    desc: {type: String},
    category: {type: String},
    order_category: {type: String}
  },
  {
    collection: "BunzlProductCrossReference"
  }
)

module.exports = {
  vars: mongoose.model("vars", vars),
  via: mongoose.model("via", via),
  collectMar: mongoose.model("collectMar", collectMar),
  collectSurr: mongoose.model("collectSurr", collectSurr),
  collectGlen: mongoose.model("collectGlen", collectGlen),
  siteNames: mongoose.model("siteNames", siteNames),
  partsQR: mongoose.model("partsQR", partsQRSchema),
  ediMetaData: mongoose.model("ediMetaData", ediMetaData),
  bunzlCrossRef: mongoose.model("bunzlCrossRef", bunzlCrossRef)
};
