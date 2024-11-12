const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
    res.render('index');
});

router.get('/selectChimney2', (req, res) => {
    res.render('selectChimney2');
});

module.exports = router;