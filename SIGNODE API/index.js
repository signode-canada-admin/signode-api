const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");

const db = require("./db");
const routes = require("./routes");

const app = express();
const apiport = 4000;

app.use(cors());
app.use(bodyParser.json());
app.use(
  bodyParser.urlencoded({
    extended: true,
  })
);

db.on("error", console.error.bind(console, "Mongo connection error"));

//api page
const path = require("path");
app.get("/api", (req, res) => {
  console.log(__dirname)
  res.sendFile(path.join(__dirname + "/pages/index.html"));
});


app.use("/api", routes);

app.get("/*", (req, res) => {
  res.redirect("/api");
});

app.listen(apiport, (err) => {
  console.log(`api at port ${apiport}`);
});
