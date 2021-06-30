const { vars, via, collectMar, collectSurr, collectGlen, siteNames } = require('../models');

const getvars = async (req, res) => {

    await vars.findOne({ _id: req.params.id }, (err, result) => {
        if (err) {
            console.log('PASS');
            return res.status(400).json({ success: false, error: err })
        }

        return res.status(200).json({ success: true, data: result })
    })
    .catch(err => { console.error(err) })

} 

const getvia = async (req, res) => {

    const arg = 'via'
    await via.findOne({ _id: `${arg}` }, (err, result)=>{
        if(err) {
            return res.status(400).json({ success: false, error: err })
        }

        return res.status(200).json({ success: true, data: result })
    })

}

const getSiteList = async (req, res) => {

    const arg = 'sites'
    await siteNames.findOne({ _id: `${ arg }` }, (err, result)=> {
        if (err){
            return res.status(400).json({ success: False, error: err })
        }

        return res.status(200).json({ success: true, data: result })
    })

} 

const getTickets = async (req, res) => {

    let site = req.params.site;

    const response = (err, result)=> {
        if (err) {
            return res.status(400).json({ success: false, error: err })
        }

        return res.status(200).json({ success: true, data: result })
    }

    if (site === 'mar'){

        await collectMar.find({  }, response)

    } else if (site === 'surr'){

        await collectSurr.find({  }, response)

    } else {

        await collectGlen.find({  }, response)

    }

}

const getOrder = async(req, res) => {

    let site = req.params.site;
    let id = req.params.id

    const response = (err, result)=> {
        if (err) {
            return res.status(400).json({ success: false, error: err })
        }

        return res.status(200).json({ success: true, data: result })
    }

    if (site === 'mar'){

        await collectMar.findOne({ _id: id }, response)

    } else if (site === 'surr'){

        await collectSurr.findOne({ _id: id }, response)

    } else {

        await collectGlen.findOne({ _id: id }, response)

    }

    
}


module.exports = {
    getvars,
    getvia,
    getSiteList,
    getTickets,
    getOrder,
};