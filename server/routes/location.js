
const express = require('express');
const router = express.Router();
const bodyParser = require('body-parser');

// body-parser 미들웨어 설정
router.use(bodyParser.urlencoded({ extended: true }));
router.use(bodyParser.json());


router.get('/', (req, res) => {
    res.render('location');
    // res.send('Hello, loca');
});


router.post('/process1', (req, res) => {
    console.log('Process 1 호출 성공');
    console.log('input data:', req.body);
    res.json({ redirect: '/' });
});

router.post('/process2', (req, res) => {
    console.log('Process 2 호출 성공');
    console.log('input data:', req.body);
    res.json({ redirect: '/' });
});

router.post('/process3', (req, res) => {
    console.log('Process 3 호출 성공');
    console.log('input data:', req.body);
    res.json({ redirect: '/' });
});

module.exports = router;
