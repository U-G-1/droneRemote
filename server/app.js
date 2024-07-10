const express = require('express');
const path = require('path');
const dotenv = require('dotenv');
const nunjucks = require('nunjucks');
const {sequelize} = require('./models');

dotenv.config();
const indexRouter = require('./routes');
const userRouter = require('./routes/user');
const pyTestRouter = require('./routes/pyTest');


const app = express();
app.set('view engine', 'ejs');
app.set('views', './views');
app.set('port', process.env.port || 3000);
// app.set('view engine', 'html');
// nunjucks.configure('./views', {
//     express: app,
//     watch: true,
// });

sequelize.sync({ force: false })
    .then(() => {
        console.log('데이터베이스 연결 성공');
    })
    .catch((err) => {
        console.log(err);
    });


app.use('/', indexRouter);
app.use('/user', userRouter);
app.use('/pyTest', pyTestRouter);

app.use((req, res, next) => {
    res.status(404).send('Not Found');
});

app.use((err, req, res, next) => {
    console.error(err);
    res.status(500).send(err.message);
});

app.listen(app.get('port'), ()=>{
    console.log(app.get('port'),'번 포트에서 대기중');
});