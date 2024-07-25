const express = require('express');
const { Location } = require('../models');
const router = express.Router();


const spawn = require('child_process').spawn;
const iconv = require('iconv-lite');


// const arges = [11,12,13]

// const result = spawn('python', ['pyCode/test.py', ...arges]);
// let rs

// result.stdout.on('data', function (data) {
//     rs = iconv.decode(data, 'euc-kr');
//     console.log(rs);
// });
// result.stdout.on('data', (data) => {
//     // Python 스크립트의 출력 데이터를 줄 단위로 나누어 배열로 변환
//     const output = data.toString().split('\n').filter(line => line.length > 0);
    
//     // 출력 결과 확인
//     console.log('Output from Python script:');
//     output.forEach((line, index) => {
//         console.log(`arg${index + 1}: ${line}`);
//     });
// });

// result.stderr.on('data', function (data) {
//     rs = iconv.decode(data, 'euc-kr');
//     console.log(rs);
// });
// result.stderr.on('data', (data) => {
//     console.error(`stderr: ${data}`);
// });

function getPythonData() {
    return new Promise((resolve, reject) => {
        const args = [11, 12, 13]; // 전달할 인자
        const pythonProcess = spawn('python', ['pyCode/test.py', ...args]);

        let output = '';
        pythonProcess.stdout.on('data', (data) => {
            output += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            reject(data.toString());
        });

        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                reject(`Python script exited with code ${code}`);
            } else {
                const result = output.split('\n').filter(line => line.length > 0);
                resolve(result);
            }
        });
    });
}

// 라우트 설정
router.get('/', async (req, res) => {
    try {
        const result = await getPythonData();

        // result 배열에서 값을 가져와 데이터베이스에 저장
        const [loca_x, loca_y, loca_z] = result.map(Number);

        await Location.create({ loca_x, loca_y, loca_z });

        res.render('index', { numbers: result });
    } catch (err) {
        res.status(500).send(err.toString());
    }
});

router.post('/process', async (req, res, next) => {
    console.log('process 호출 성공');
    console.log('input data : ', req.body);
    res.redirect('/pyTest');
});

module.exports = router;