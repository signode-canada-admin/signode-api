const express = require('express');
const ctrl = require('../route-ctrl');

const router = express.Router()

router.get('/vars/:id', ctrl.getvars);
router.get('/via', ctrl.getvia);
router.get('/sites', ctrl.getSiteList);
router.get('/tickets/:site', ctrl.getTickets);
router.get('/tickets/:site/:id', ctrl.getOrder);
router.get('/tickets/:site/:id/page', ctrl.getPage)
router.get('/*', (req, res)=>{
    res.redirect('/api')
})

module.exports = router;