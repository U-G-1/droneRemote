const express = require('express');
const { exec } = require('child_process');
const router = express.Router();

// GET 요청 시 location.ejs를 렌더링
router.get('/', (req, res) => {
    res.render('location');
});

// POST 요청 시 파이썬 스크립트를 실행
router.post('/execute', (req, res) => {
    console.log('드론 이동 실행');
    const chimney = req.body.chimney;
    console.log('굴뚝 번호: ', req.body.chimney);
    const scriptPath = `pyCode/drone_test.py ${chimney}`;

    exec(`python ${scriptPath}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing script: ${error}`);
            return res.status(500).send(`Error: ${error.message}`);
        }
        if (stderr) {
            console.error(`Script stderr: ${stderr}`);
            return res.status(500).send(`Script stderr: ${stderr}`);
        }
        console.log(`Script stdout: ${stdout}`);
        res.send(`Script executed successfully: ${stdout}`);
    });
});

module.exports = router;
