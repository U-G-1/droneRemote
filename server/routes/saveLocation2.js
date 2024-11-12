const express = require('express');
const router = express.Router();


router.post('/', (req, res) => {
    const chimneyNumber = req.body.chimneyNumber;
    console.log(`Selected chimney number: ${chimneyNumber}`);
    res.render('saveLocation2', { chimneyNumber });
});



module.exports = router;
