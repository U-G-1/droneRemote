const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const router = express.Router();
const { Location } = require('../models'); // Location 모델을 가져옵니다.


// GET 요청 시 location.ejs를 렌더링
router.get('/', (req, res) => {
    res.render('moveDrone');
});

// POST 요청 시 파이썬 스크립트를 실행
router.post('/move',async (req, res) => {
    console.log('드론 이동 실행');
    const chimneyNumber = req.body.chimney; // 선택된 굴뚝 번호를 가져옵니다.
    const chimName = `굴뚝${chimneyNumber}`; // 선택된 굴뚝 번호에 해당하는 이름을 생성합니다.

    // 데이터베이스에서 해당 chim_name을 가진 Location을 검색합니다.
    const location = await Location.findOne({ where: { chim_name: chimName } });

    if (!location) {
        return res.status(404).send('Chimney not found');
    }

    // 좌표 값을 변수에 저장합니다.
    const x = location.loca_x;
    const y = location.loca_y;
    const z = location.loca_z;
    const slope = location.slope;

        // 측정값 콘솔
        console.log('x :', x);
        console.log('y :', y);
        console.log('z :', z);


    // 파이썬 스크립트 경로 설정
    const scriptPath = path.join(__dirname, '..', 'pyCode', 'moveDrone.py');

    // 파이썬 스크립트를 spawn으로 실행 매개변수 : chimney
    const pythonProcess = spawn('python', ['-u',scriptPath, x,y,z,slope]);

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
            res.redirect('/moveDrone');
        } else {
            res.status(500).send(`Script failed with code ${code}`);
        }
    });
});

module.exports = router;
