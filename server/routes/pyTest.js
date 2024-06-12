const express = require('express');

const router = express.Router();


const spawn = require('child_process').spawn;
const iconv = require('iconv-lite');
let num1 = 10
let num2 = 10

const result = spawn('python', ['pyCode/test.py', num1, num2]);
let rs

result.stdout.on('data', function (data) {
    rs = iconv.decode(data, 'euc-kr');
    console.log(rs);
});
result.stderr.on('data', function (data) {
    rs = iconv.decode(data, 'euc-kr');
    console.log(rs);
});

router.get('/', (req, res) => {  
    res.render('index', {number: rs});
});

module.exports = router;