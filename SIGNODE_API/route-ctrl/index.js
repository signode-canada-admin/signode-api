const fs = require("file-system");
const PDFDocument = require("pdfkit");
const blobStream = require("blob-stream");
require('dotenv').config();

//
//GLOBAL DB
let db = {
  "data": [],
  "pdfs": [],
  "urls" : []
}

const SITES = {
  "pp": "Premium_plus",
  "srap": "Srap",
  "bi": "Bunzl_industrial"
}
//

const {
  vars,
  via,
  collectMar,
  collectSurr,
  collectGlen,
  siteNames,
  partsQR,
  ediMetaData,
  bunzlCrossRef,
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

const getSitePdfs = async (req, res) => {
  let site = req.params.site
  const spawn = require("child_process").spawn;
  const siteName = SITES[site]
  const fileDir = process.env.COMMON_FILES_LIST
  // if (site==='pp'){
  //   siteName = SITES[site]
  //   fileDir = process.env.COMMON_FILES_LIST
  // } else if (site === 'bi') {
  //   siteName = SITES[site]
  //   fileDir = `${process.env.PP_TABULA}/get_list_of_files.py`
  // } else if (site==='srap') {
  //   siteName = SITES[site]
  //   fileDir = `${process.env.PP_TABULA}/get_list_of_files.py`
  // }
  const pythonProcess = await spawn('python',[`${fileDir}`, `${siteName}`]);
  pythonProcess.stdout.on('data', (data) => {
      data = data.toString().replace(/'/g, '"')
      const pdfList = JSON.parse(data)
      if (pdfList.success != "false"){
        return res.status(200).json(pdfList)  
      }
      return res.status(404).json(pdfList)
  });
}


const getEDIpageExtract = async (req, res) => {
  let site = req.params.site;
  let id = req.params.id;

  const spawn = require("child_process").spawn;
  
  // const file = `Y:\\Pick Ticket Project\\EDI\\Premium_plus\\PDFS_PREMIUM_PLUS\\${id}.pdf`
  let fileDir = `${process.env.BASE_URL}/edi/${site}/${id}`
  let pythonFile =  ``
  let URL = ``
  if (site==='pp'){
    pythonFile = process.env.PP_TABULA
  } else if (site === 'bi') {
    pythonFile = process.env.BI_TABULA
  } else if (site==='srap') {
    pythonFile = process.env.SRAP_TABULA
  } else if (site==='am') {
    pythonFile = process.env.AM_TABULA
  } else if (site==='srap_tr') {
    pythonFile = process.env.SRAP_TR_TABULA
  }

  function bi_extract (pythonFile, fileDir) {
    const pythonProcess = spawn('python', [pythonFile, fileDir]);
    pythonProcess.stdout.on('data', (data) => {
        data = data.toString().replace(/'/g, '"')
        const pdfData = JSON.parse(data)
        return res.status(200).json({success: true, pdfData: pdfData})
    });
  }

  function extract (pythonFile, fileDir) {
    const pythonProcess = spawn('python', [pythonFile, fileDir]);
    pythonProcess.stdout.on('data', (data) => {
        data = data.toString().replace(/'/g, '"')
        const pdfData = JSON.parse(data)
        return res.status(200).json({success: true, pdfData: pdfData})
    });
  }
  

  if (site!=='bi') {
    extract(pythonFile, fileDir)
  } else {
    bi_extract(pythonFile, fileDir)
  }
  
  // const pythonProcess = spawn('python', [pythonFile, fileDir]);
  // pythonProcess.stdout.on('data', (data) => {
  //     data = data.toString().replace(/'/g, '"')
  //     const pdfData = JSON.parse(data)
  //     return res.status(200).json({success: true, pdfData: pdfData})
  // });


}

const getEdipage = async (req, res) => {
  let id = req.params.id;
  let site = req.params.site;
  let archived = req.query.archived;

  const response = (err, result) => {
    if (err || !result) {
      return res.status(400).json({
        success: false,
        error: `${err ? err : "wrong order# specified"}`,
      });
    }
    let fileDir = '';
    if (site==='pp'){
      if (archived==='true'){
        fileDir = `${process.env.PP_ARCHIVED_URL}\\${id}.pdf`
      } else {
        fileDir = `${process.env.PP_URL}\\${id}.pdf`
      }
    } else if (site==='bi') {
      if (archived==='true') {
        fileDir = `${process.env.BI_ARCHIVED_URL}\\${id}.pdf`
      } else {
        fileDir = `${process.env.BI_URL}\\${id}.pdf`
      }
    } else if (site==='srap') {
      if (archived === 'true') {
        fileDir = `${process.env.SRAP_ARCHIVED_URL}\\${id}.pdf`
      } else {
        fileDir = `${process.env.SRAP_URL}\\${id}.pdf`
      }
    } else if (site==='srap_tr'){
      if (archived === 'true'){
        fileDir = `${process.env.SRAP_TR_ARCHIVED_URL}\\${id}.pdf`
      } else {
        fileDir = `${process.env.SRAP_TR_URL}\\${id}.pdf`
      }
    } else if (site==='am'){
      if (archived === 'true'){
        fileDir = `${process.env.AM_ARCHIVED_URL}\\${id}.pdf`
      } else {
        fileDir = `${process.env.AM_URL}\\${id}.pdf`
      }
    }

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


const ediMeta = async (req, res) => {
  const site = req.params.site;
  const response = (err, result) => {
    if (err) {
      return res.status(400).json({ success: false, error: err });
    }

    return res.status(200).json({ success: true, data: result });
  };
  ediMetaData.findOne({customer: site}, response)
}

const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

const postEdiDetails = async (req, res) => {
  let post_data = req.body;
  const id = req.params.id;
  let site = req.params.site;

  // const metaURL = `http://localhost:4000/api/edimetadata/${site}`
  const metaURL = `${process.env.BASE_URL}/edimetadata/${site}`
  // const metaURL = `http://localhost:4000/api/edimetadata/pp`
  const fetch_meta = await fetch(metaURL)
  const fetch_res = await fetch_meta.json()

  // let fileDir = `${process.env.BASE_URL}/edi/${site}/${id}`
  let pythonFile = '';
  const poMeta = fetch_res.data.data;
  let excel_data = {"line_items": []}
  excel_data.ship_via = post_data.ship_via
  excel_data.po_no = post_data.po_no
  excel_data.customer_name = poMeta.customer_name
  excel_data.ship_to = poMeta.ship_to
  excel_data.warehouse = poMeta.warehouse
  excel_data.order_type = poMeta.order_type
  excel_data._id = id


  if (Array.isArray(post_data.prod_no)) {
      post_data.prod_no.forEach((prod, i) => {
          excel_data.num_line_items = post_data.prod_no.length
          excel_data.line_items.push({"quantity": post_data.prod_qty[i], "product": prod})
      })
  } else {
      excel_data.num_line_items = 1
      excel_data.line_items.push({"quantity": post_data.prod_qty, "product": post_data.prod_no})
  }

  // add to db
  site = SITES[site]
  db.data.push(excel_data)
  db.pdfs.push(`${id}*SEPARATOR*${site}`)
  // db.urls.push(`${process.env.EDI_CUSTOMERS}\\${SITES[site]}\\${id}.pdf`)

  res.redirect(`${process.env.BASE_WEB_URL}/edi/DONE?id=${site} ${id}`)
  // res.redirect(`http://localhost:3000/edi/DONE?id=${site} ${id}`)
}

const ediDBMetaData = (req, res) => {
  return res.status(200).json(db)
}

const createSX = async (req, res) => {
  //access python file
  const spawn = require("child_process").spawn;
  const pythonProcess = spawn('python', [process.env.COMMON_ONE_SHEET, JSON.stringify(db)]);
  pythonProcess.stdout.on('data', (data) => {
      data = data.toString().replace(/'/g, '"')
      const pdfData = JSON.parse(data)
      // console.log(pdfData)
      // empty db
      db = {"data": [], "pdfs": []}
      res.status(200).json({"success": true})
      // console.log("DONE")
      // if (pdfData.success !== 'false') {
      //   res.redirect("http://localhost:3000/edi")
      // } else {
      //   res.redirect(`http://localhost:3000/edi/DONE?id=DONE`)
      // }
  });

  

  //initiate function arguments

  //process python

  //empty the EDI GLOBAL DB

  //return response
}

const getbunzlCrossRef = async (req, res) => {
  const query = req.query
  
  const response = (err, data) => {
    if (err) {
      res.status(400).json({success: false, error: err})
    }
    res.status(200).json({success: true, data: data})
  }
  await bunzlCrossRef.find(query, response)
}


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
  getSitePdfs,
  getEdipage,
  getEDIpageExtract,
  postEdiDetails,
  ediMeta,
  createSX,
  ediDBMetaData,
  getbunzlCrossRef,
};
