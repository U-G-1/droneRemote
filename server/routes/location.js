const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
//const { io } = require('../app');
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


    let scriptPath;

    if(chimney==1){
        // 파이썬 스크립트 경로 설정
        scriptPath = path.join(__dirname, '..', 'pyCode', 'drone_land_test.py');
    }else if(chimney==2){
        scriptPath = path.join(__dirname, '..', 'pyCode', 'drone_save_test.py');
    }else if(chimney==3) {
        scriptPath = path.join(__dirname, '..', 'pyCode', 'drone_arming_test.py');
    }

    // 스크립트 경로가 설정되지 않은 경우 오류 반환
    if (!scriptPath) {
        return res.status(400).send('Invalid value');
    }

    // 파이썬 스크립트를 spawn으로 실행 매개변수 : chimney
    const pythonProcess = spawn('python', ['-u',scriptPath]);

    // 스크립트 실행 중 표준 출력 처리
    pythonProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
        global.io.emit('consoleMessage', data.toString());
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
