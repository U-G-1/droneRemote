const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const router = express.Router();

// GET 요청 시 location.ejs를 렌더링
router.get('/', (req, res) => {
    res.render('location');
});

// POST 요청 시 파이썬 스크립트를 실행
router.post('/execute', (req, res) => {
    console.log('드론 이동 실행');
    const chimney = req.body.chimney;
    console.log('굴뚝 번호: ', chimney);

    // 파이썬 스크립트 경로 설정
    const scriptPath = path.join(__dirname, '..', 'pyCode', 'drone_test.py');

    // 파이썬 스크립트를 spawn으로 실행 매개변수 : chimney
    const pythonProcess = spawn('python', [scriptPath, chimney]);

    // 스크립트 실행 중 표준 출력 처리
    pythonProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
    });

    // 스크립트 실행 중 표준 오류 처리
    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    // 스크립트 실행 종료 시 처리
    pythonProcess.on('close', (code) => {
        if (code === 0) {
            res.send('Script executed successfully');
        } else {
            res.status(500).send(`Script failed with code ${code}`);
        }
    });
});

module.exports = router;