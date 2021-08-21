const express = require('express');
const {spawn} = require('child_process');
const path = require('path');
const app = express();

app.use(express.json({limit: '500mb'}));


app.post('/encode', (req, res) => {
    const {encodedata} = req.body;
    const task = spawn('python', [path.join(__dirname, 'PYTHON', 'encode.py'), encodedata.toString()]);
    var outpututf8str = "";
    task.stdout.on('data', data => {
        outpututf8str += data.toString();
      });

    task.on('close', (code) => {
        res.send({
            output : `${outpututf8str}`
        })
    });
}
);

app.post('/decode', (req, res) => {
    const {decodedata} = req.body;
    const task = spawn('python', [path.join(__dirname, 'PYTHON', 'decode.py'), decodedata.toString()]);
    var outpututf8str = "";
    task.stdout.on('data', data => {
        outpututf8str += data.toString();
      });

    task.on('close', (code) => {
        res.send({
            output : `${outpututf8str}`
        })
    });


}
);



const port = process.env.PORT || 8080;

app.listen(
    port,
    () => console.log(`listening on ${port}`)
);