const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
    res.render('selectChimny2');
});

router.post('/saveLocation2', (req, res) => {
    const chimneyNumber = req.body.chimneyNumber;
    console.log(`Selected chimney number: ${chimneyNumber}`);
    res.redirect('/saveLocation2');  
});

module.exports = router;
