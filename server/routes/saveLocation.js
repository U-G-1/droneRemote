const express = require('express');
const { Location } = require('../models'); // 모델 가져오기
const { spawn } = require('child_process');
const path = require('path');
const router = express.Router();


router.get('/', (req, res) => {
    // Python 스크립트를 실행합니다.
    const pythonProcess = spawn('python3', ['-u','pyCode/saveLocation.py']);

    let output = '';

    // Python 스크립트의 표준 출력을 받습니다.
    pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
    });
    let x, y, z;  // 라우터 외부에서 선언
    // Python 스크립트가 완료된 후 실행됩니다.
    pythonProcess.on('close', (code) => {
        if (code !== 0) {
            return res.status(500).send(`Python script exited with code ${code}`);
        }

        // 출력된 값을 배열로 변환하여 EJS로 전달합니다.
        const values = output.split('\n').filter(line => line.trim() !== '');
        const [xRaw, yRaw, zRaw] = output.split('\n').filter(line => line.trim() !== '');
        x = parseFloat(xRaw);
        y = parseFloat(yRaw);
        z = parseFloat(zRaw);
        res.render('saveLocation', { values });

        // 측정값 콘솔
        console.log('values : ',values);
        console.log('x :', x);
        console.log('y :', y);
        console.log('z :', z);
    });
    router.post('/save', async (req, res) => {
        try {
            const { chim_name } = req.body;

            //같은 굴뚝이름의 최대 번호를 가져옴
            const maxChimNum = await Location.max('chim_num', {
                where: { chim_name: chim_name }
            });
            const chim_num = maxChimNum !== null ? maxChimNum + 1 : 1;
    
            // 데이터베이스에 저장
            await Location.create({
                loca_x: x,
                loca_y: y,
                loca_z: z,
                slope: 0, // slope 값을 0으로 설정
                chim_name: chim_name,
                chim_num: chim_num
            });
            // 저장 완료 후 /saveLocation 페이지로 메시지와 함께 리디렉션
            res.redirect('/');
        } catch (err) {
            console.error('Error saving location:', err);
            res.status(500).send('Error saving location');
        }
    });
});


module.exports = router;