const fs = require("file-system");
const PDFDocument = require("pdfkit");
const blobStream = require("blob-stream");

const {
  vars,
  via,
  collectMar,
  collectSurr,
  collectGlen,
  siteNames,
  partsQR,
} = require("../models");

const getvars = async (req, res) => {
  await vars
    .findOne({ _id: req.params.id }, (err, result) => {
      if (err) {
        return res.status(400).json({ success: false, error: err });
      }

      return res.status(200).json({ success: true, data: result });
    })
    .catch((err) => {
      console.error(err);
    });
};

const getvia = async (req, res) => {
  const arg = "via";
  await via.findOne({ _id: `${arg}` }, (err, result) => {
    if (err) {
      return res.status(400).json({ success: false, error: err });
    }

    return res.status(200).json({ success: true, data: result });
  });
};

const getSiteList = async (req, res) => {
  const arg = "sites";
  await siteNames.findOne({ _id: `${arg}` }, (err, result) => {
    if (err) {
      return res.status(400).json({ success: False, error: err });
    }

    return res.status(200).json({ success: true, data: result });
  });
};

const getTickets = async (req, res) => {
  let site = req.params.site;

  const response = (err, result) => {
    if (err) {
      return res.status(400).json({ success: false, error: err });
    }

    return res.status(200).json({ success: true, data: result });
  };

  if (site === "markham") {
    await collectMar.find({}, response);
  } else if (site === "surrey") {
    await collectSurr.find({}, response);
  } else if (site === "glenview") {
    await collectGlen.find({}, response);
  } else {
    return res
      .status(400)
      .json({ success: false, err: "wrong site specified" });
  }
};

const getStatus = async (req, res) => {
  const capitalize = (word) => {
    return word.charAt(0).toUpperCase() + word.slice(1);
  };

  let site = req.params.site;
  let stat = { status: capitalize(req.params.status) };

  const response = (err, result) => {
    if (err) {
      return res.status(400).json({ success: false, error: err });
    }

    return res.status(200).json({ success: true, data: result });
  };

  if (site === "markham") {
    await collectMar.find(stat, response);
  } else if (site === "surrey") {
    await collectSurr.find(stat, response);
  } else if (site === "glenview") {
    await collectGlen.find(stat, response);
  } else {
    return res
      .status(400)
      .json({ success: false, err: "wrong site specified" });
  }
};

const getOrder = async (req, res) => {
  let site = req.params.site;
  let id = req.params.id;

  const response = (err, result) => {
    if (err) {
      return res.status(400).json({ success: false, error: err });
    }

    return res.status(200).json({ success: true, data: result });
  };

  if (site === "markham") {
    await collectMar.findOne({ _id: id }, response);
  } else if (site === "surrey") {
    await collectSurr.findOne({ _id: id }, response);
  } else if (site === "glenview") {
    await collectGlen.findOne({ _id: id }, response);
  } else {
    return res
      .status(400)
      .json({ success: false, err: "wrong site specified" });
  }
};

const getPage = async (req, res) => {
  let site = req.params.site;
  let id = req.params.id;

  const response = (err, result) => {
    if (err || !result) {
      return res.status(400).json({
        success: false,
        error: `${err ? err : "wrong order# specified"}`,
      });
    }

    let fileDir = result.fileDirectory;

    fs.stat(fileDir, function (err, stat) {
      if (err == null) {
        let stream = fs.createReadStream(`${fileDir}`);
        let fileName = result.easyName;
        fileName = encodeURIComponent(fileName);

        res.setHeader(
          "Content-disposition",
          'inline; filename="' + fileName + '"'
        );
        res.setHeader("Content-type", "application/pdf");

        stream.pipe(res);
      } else if (err.code === "ENOENT") {
        return res.status(400).json({
          success: false,
          error: `${
            err
              ? err
              : "specified file not found, please check onedrive file location"
          }`,
        });
      } else {
        return res.status(400).json({
          success: false,
          error: `${
            err ? err : "Some other error occurred whiel accessing this file"
          }`,
        });
      }
    });
  };

  if (site === "markham") {
    await collectMar.findOne({ _id: id }, response);
  } else if (site === "surrey") {
    await collectSurr.findOne({ _id: id }, response);
  } else if (site === "glenview") {
    await collectGlen.findOne({ _id: id }, response);
  } else {
    return res
      .status(400)
      .json({ success: false, err: "wrong site specified" });
  }
};

const getSearch = async (req, res) => {
  const site = req.params.site;
  const searchQuery = req.params.query;

  const response = (err, result) => {
    if (err) {
      return res.status(400).json({ success: false, error: err });
    }

    return res.status(200).json({ success: true, data: result });
  };

  if (site === "markham") {
    await collectMar
      .find(
        { $text: { $search: `${searchQuery}` } },
        { score: { $meta: "textScore" } },
        response
      )
      .sort({ score: { $meta: "textScore" } })
      .sort({ dateReceived: -1 });
  } else if (site === "surrey") {
    await collectSurr
      .find(
        { $text: { $search: `\"${searchQuery}\"` } },
        { score: { $meta: "textScore" } },
        response
      )
      .sort({ score: { $meta: "textScore" } })
      .sort({ dateReceived: -1 });
  } else if (site === "glenview") {
    await collectGlen
      .find(
        { $text: { $search: `\"${searchQuery}\"` } },
        { score: { $meta: "textScore" } },
        response
      )
      .sort({ score: { $meta: "textScore" } })
      .sort({ dateReceived: -1 });
  } else {
    return res
      .status(400)
      .json({ success: false, err: "wrong site specified" });
  }
};


const getEdipage = async (req, res) => {
  let id = req.params.id;

  const response = (err, result) => {
    if (err || !result) {
      return res.status(400).json({
        success: false,
        error: `${err ? err : "wrong order# specified"}`,
      });
    }

    let fileDir = `Y:\\Pick Ticket Project\\EDI\\Premium_plus\\PDFS_PREMIUM_PLUS\\${id}.pdf`

    fs.stat(fileDir, function (err, stat) {
      if (err == null) {
        let stream = fs.createReadStream(`${fileDir}`);
        fileName = encodeURIComponent(id);

        res.setHeader(
          "Content-disposition",
          'inline; filename="' + fileName + '"'
        );
        res.setHeader("Content-type", "application/pdf");

        stream.pipe(res);
      } else if (err.code === "ENOENT") {
        return res.status(400).json({
          success: false,
          error: `${
            err
              ? err
              : "specified file not found, please check onedrive file location"
          }`,
        });
      } else {
        return res.status(400).json({
          success: false,
          error: `${
            err ? err : "Some other error occurred whiel accessing this file"
          }`,
        });
      }
    });
  };

  await response('', id)

};

const postTest = async (req, res) => {
  if (!req.body._id) {
    return res
      .status(400)
      .json({ success: false, error: "_id found to be empty" });
  }

  const id = {
    _id: req.body._id,
    createdAt: new Date().toISOString(),
  };

  console.log(`new _id found ${req.body._id}`);

  const response = (err, result) => {
    if (err) {
      return res.status(400).json({ success: false, error: err });
    }

    const doc = new PDFDocument();
    var stream = doc.pipe(blobStream());

    doc.fontSize(25).text("here is some text", 100, 80);

    doc.end();

    stream.on("finish", () => {
      iframe.src = stream.toBlobURL("application/pdf");
    });

    return res.status(200).json({ success: true, data: result });
  };

  await partsQR.findOne({ _id: req.body._id }, response);
};



async function getRedirect(req, res) {
  return res.status(404).json({ success: false, err: "Wrong URL Specified" });
}

module.exports = {
  getvars,
  getvia,
  getSiteList,
  getTickets,
  getOrder,
  getPage,
  getSearch,
  getRedirect,
  getStatus,
  postTest,
  getEdipage,
};
