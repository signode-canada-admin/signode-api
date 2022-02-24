const { MongoClient } = require("mongodb");

const uri = "mongodb://127.0.0.1:27017/";
const dbName = "signode";

const collectMar = "markham";
const collectPartsQR = "partsQR";

const client = new MongoClient(uri, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

client.connect();

const database = client.db(dbName);

const markham = database.collection(collectMar);
const qr = database.collection(collectPartsQR);

const response = (err, result) => {
  if (err) {
    return err;
  }
  return result;
};

const query = {
  shipTo: "text",
  PO: "text",
  via: "text",
  status: "text",
  month: "text",
  easyName: "text",
};

// markham
//   .createIndex({ shipTo: "text" })
//   .then((res) => {
//     return "DONE";
//   })
//   .catch((err) => {
//     console.log(err);
//   });

// qr.insertOne({ _id: 1, body: "part 1" }, response);

qr.findOne({ _id: 1 }, (err, response) =>
  err ? console.log(err) : console.log(response)
);
