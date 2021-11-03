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
router.get("/edi/:id", ctrl.getEdipage);
router.get("/search/:site/:query", ctrl.getSearch);
router.get("/testapi", ctrl.postTest);
router.get("/*", ctrl.getRedirect);

module.exports = router;
