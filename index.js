const express = require('express');
const app = express();
const PORT = 8081;
const BPCS = require('./CPP/build/Release/main');


app.use(express.json({limit: '500mb'}));


app.listen(
    PORT,
    () => console.log(`listening on ${PORT}`)
);

app.get('/encode', (req, res) => {



}
);

app.get('/decode', (req, res) => {



}
);