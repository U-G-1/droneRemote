// server/routes/socket_test.js
const express = require('express');
const router = express.Router();
const { io } = require('../app'); // `app.js`에서 `io`를 가져옵니다

router.get('/', (req, res) => {
    res.render('socket_test');
    printNumbers();
});

function printNumbers() {
    let count = 1;
    const intervalId = setInterval(() => {
        console.log(count); // 콘솔에 숫자 출력

        // 클라이언트로 숫자 메시지 전송
        if (io) {
            io.emit('consoleMessage', `Number: ${count}`);
        } else {
            console.error('io is not defined');
        }

        if (count === 10) {
            clearInterval(intervalId); // 10에 도달하면 타이머 종료
        }

        count++;
    }, 1000); // 1초마다 실행
}

module.exports = router;
