const express = require('express');
const ctrl = require('../route-ctrl');

const router = express.Router()

router.get('/vars/:id', ctrl.getvars);
router.get('/via', ctrl.getvia);
router.get('/tickets/:site', ctrl.getTickets);
router.get('/tickets/:site/:id', ctrl.getOrder);

module.exports = router;