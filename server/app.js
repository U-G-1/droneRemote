const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
// const path = require('path');
const dotenv = require('dotenv');
// const nunjucks = require('nunjucks');
const {sequelize} = require('./models');
const bodyParser = require('body-parser');

dotenv.config();
const indexRouter = require('./routes');
const userRouter = require('./routes/user');
const pyTestRouter = require('./routes/pyTestt');
const locaRouter = require('./routes/location');
const saveLocationRouter = require('./routes/saveLocation');
const moveDroneRouter = require('./routes/moveDrone');
const socketRouter = require('./routes/socket_test');


const app = express();

const server = http.createServer(app);   // Express 앱을 기반으로 HTTP 서버 생성
const io = socketIo(server);


app.set('view engine', 'ejs');
app.set('views', './views');
app.set('port', process.env.port || 3000);
// app.set('view engine', 'html');
// nunjucks.configure('./views', {
//     express: app,
//     watch: true,
// });

//DB 연결
sequelize.sync({ force: false })
    .then(() => {
        console.log('데이터베이스 연결 성공');
    })
    .catch((err) => {
        console.log(err);
    });

    // Body parser middleware
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Socket.io 설정
io.on('connection', (socket) => {
    console.log('a user connected');
  
    socket.on('disconnect', () => {
      console.log('user disconnected');
    });
  });

app.use('/', indexRouter);
app.use('/user', userRouter);
app.use('/pyTest', pyTestRouter);
app.use('/location', locaRouter);
app.use('/saveLocation', saveLocationRouter);
app.use('/moveDrone', moveDroneRouter);
app.use('/socketTest', (req, res, next) => {
    req.io = io; // `req` 객체에 `io`를 추가
    next();
}, socketRouter);

app.use((req, res, next) => {
    res.status(404).send('Not Found');
});

app.use((err, req, res, next) => {
    console.error(err);
    res.status(500).send(err.message);
});


// Socket.IO connection
// io.on('connection', (socket) => {
//     console.log('A user connected');

//     // Send a message to the client when a user connects
//     socket.emit('consoleMessage', 'Connected to server');

//     // Listen for console messages from the server
//     process.stdout.write = (function(write) {
//         return function(string, encoding, fd) {
//             socket.emit('consoleMessage', string);
//             write.apply(process.stdout, arguments);
//         };
//     })(process.stdout.write);

//     // Handle disconnection
//     socket.on('disconnect', () => {
//         console.log('A user disconnected');
//     });
// });

// Export `io` for use in other modules
// module.exports = { io };

// Export `io` and `server` for use in other modules
module.exports = { io, server };



server.listen(app.get('port'), ()=>{
    console.log(app.get('port'),'번 포트에서 대기중');
});