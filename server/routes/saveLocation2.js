const express = require('express');
const cookieParser = require('cookie-parser');
const router = express.Router();

router.use(cookieParser());

router.post('/', (req, res) => {
    const chimneyNumber = req.body.chimneyNumber;
    
    // 굴뚝 번호를 쿠키로 설정
    res.cookie('chimneyNumber', chimneyNumber, {
        httpOnly: true, // 클라이언트에서 JavaScript로 접근 불가 (보안 강화)
        maxAge: 24 * 60 * 60 * 1000, // 1일 유지
    });
    
    console.log(`Selected chimney number: ${chimneyNumber}`);
    res.render('saveLocation2', { values: [] });
});

let x, y, z;  // 라우터 외부에서 선언
// 측정
router.post('/measure', (req, res) => {
    // 쿠키에서 굴뚝 번호 읽기
    const chimneyNumber = req.cookies.chimneyNumber;

    if (!chimneyNumber) {
        return res.status(400).send('Chimney number not set in cookie.');
    }
    //굴뚝번호 유지 확인
    console.log(`Selected chimney number: ${chimneyNumber}`);
    const scriptPath = './pyCode/saveLocation.py';
    const pythonProcess = spawn('python', ['-u', scriptPath]);

    pythonProcess.stdout.on('data', (data) => {
        console.log(`Python stdout: ${data}`);
        global.io.emit('consoleMessage', data.toString());
        output += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python stderr: ${data}`);
        global.io.emit('consoleMessage', data.toString());
    });

    pythonProcess.on('close', (code) => {
        // if (code === 0) {
        //     //*****리다이렉트 보류 : 리다이렉트 하지 않을시 페이지가 어떻게 되는지 확인, 굴뚝번호 값도 확인
        //     // res.redirect('/saveLocation2', { chimneyNumber }); // 완료 후 다시 페이지 리로드, xyz값도 전달해야할지 확인
        // } else {
        //     res.status(500).send(`Python script failed with code ${code}`);
        // }
        if (code !== 0) {
            return res.status(500).send(`Python script exited with code ${code}`);
        }
        // 출력된 값을 배열로 변환하여 EJS로 전달합니다.
        const values = output.split('\n').filter(line => line.trim() !== '');
        const [xRaw, yRaw, zRaw] = output.split('\n').filter(line => line.trim() !== '');
        x = parseFloat(xRaw);
        y = parseFloat(yRaw);
        z = parseFloat(zRaw);
        res.render('saveLocation2', { values });

        // 측정값 콘솔
        console.log('values : ',values);
        console.log('x :', x);
        console.log('y :', y);
        console.log('z :', z);
    });
});

// 추가
router.post('/add', async (req, res) => {
    const chimneyNumber = req.cookies.chimneyNumber;

    //같은 굴뚝이름의 최대 번호를 가져옴
    const maxChimNum = await Location.max('chim_num', {
        where: { chim_name: chimneyNumber } //*** */
    });
    const chim_num = maxChimNum !== null ? maxChimNum + 1 : 1;


    try {
        await Location.create({
            loca_x: x, // 데이터베이스 `loca_x` 필드에 저장
            loca_y: y, // 데이터베이스 `loca_y` 필드에 저장
            loca_z: z, // 데이터베이스 `loca_z` 필드에 저장
            slope:0, // `slope` 필드에 저장
            chim_name: chimneyNumber,
            chim_num: chim_num
        });

        res.redirect('/saveLocation2', { values }); 
        
    } catch (error) {
        console.error('Error saving location:', error); 
        // 데이터베이스 작업 중 오류가 발생하면 콘솔에 출력
        res.status(500).send('Error saving location'); 
        // 500 상태 코드와 함께 오류 메시지 전송
    }
});





module.exports = router;
