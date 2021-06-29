const express = require('express');
const ctrl = require('../route-ctrl');

const router = express.Router()

router.get('/vars/:id', ctrl.getvars);
router.get('/via', ctrl.getvia);
router.get('/tickets/mar', ctrl.getMar);

module.exports = router;