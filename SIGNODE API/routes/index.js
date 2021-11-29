const express = require("express");
const ctrl = require("../route-ctrl");

const router = express.Router();

router.get("/vars/:id", ctrl.getvars);
router.get("/via", ctrl.getvia);
router.get("/sites", ctrl.getSiteList);
router.get("/tickets/:site", ctrl.getTickets);
router.get("/tickets/:site/:status", ctrl.getStatus);
router.get("/tickets/:site/:id", ctrl.getOrder);
router.get("/tickets/:site/:id/page", ctrl.getPage);
router.get("/edi/:site/pdfs", ctrl.getSitePdfs)
router.get("/edi/:site/:id", ctrl.getEdipage);
router.get("/edi/:site/:id/extract", ctrl.getEDIpageExtract)
router.post("/edi/:site/:id/post", ctrl.postEdiDetails)
router.get("/edi/createSX", ctrl.createSX)
router.get("/edimetadata", ctrl.ediDBMetaData)
router.get("/edimetadata/:site", ctrl.ediMeta)
router.get("/search/:site/:query", ctrl.getSearch);
router.get("/testapi", ctrl.postTest);
router.get("/*", ctrl.getRedirect);

module.exports = router;
