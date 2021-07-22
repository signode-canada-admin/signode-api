const { vars, via, collectMar, collectSurr, collectGlen, siteNames } = require('../models');

const getvars = async (req, res) => {

    await vars.findOne({ _id: req.params.id }, (err, result) => {
        if (err) {
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

    if (site === 'markham'){

        await collectMar.find({  }, response)

    } else if (site === 'surrey'){

        await collectSurr.find({  }, response)

    } else if (site === 'glenview'){

        await collectGlen.find({  }, response)

    } else {

        return res.status(400).json({ success: false, err: 'wrong site specified' })
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

    if (site === 'markham'){

        await collectMar.findOne({ _id: id }, response)

    } else if (site === 'surrey'){

        await collectSurr.findOne({ _id: id }, response)

    } else if (site === 'glenview'){

        await collectGlen.findOne({ _id: id }, response)

    } else {

        return res.status(400).json({ success: false, err: 'wrong site specified' })
    }
    
}


module.exports = {
    getvars,
    getvia,
    getSiteList,
    getTickets,
    getOrder,
};