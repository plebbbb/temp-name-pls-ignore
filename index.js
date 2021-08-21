const express = require('express');
const {spawn} = require('child_process');
const app = express();
const PORT = 8080;


app.use(express.json({limit: '500mb'}));


app.get('/encode', (req, res) => {
    const {encodedata} = req.body;
    const task = spawn('python', ['./PYTHON/encode.py', encodedata.toString()]);
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

app.get('/decode', (req, res) => {
    const {decodedata} = req.body;
    const task = spawn('python', ['./PYTHON/decode.py', decodedata.toString()]);
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


app.listen(
    PORT,
    () => console.log(`listening on ${PORT}`)
);