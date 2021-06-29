const { vars, via, collectMar } = require('../models');

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

const getMar = async (req, res) => {

    await collectMar.find({  }, (err, result)=> {
        if (err) {
            return res.status(400).json({ success: false, error: err })
        }

        return res.status(200).json({ success: true, data: result })
    })

}


module.exports = {
    getvars,
    getvia,
    getMar,
};