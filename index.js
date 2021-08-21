const express = require('express');
const {spawn} = require('child_process');
const path = require('path');
const app = express();

app.use(express.json({limit: '500mb'}));

//afaik the spec for GET says that the body of the sending side should be ignored, so we aren't using it
//not like post is better though, as technically we shouldn't be dumping an entire file back at the client
app.post('/encode', (req, res) => {
    const {encodedata} = req.body;
    const buf = Buffer.from(encodedata, 'base64').toString('utf-8');
    const {key} = req.body;
    const task = spawn('python', [path.join(__dirname, 'PYTHON', 'encode.py'), buf, key.toString()]);
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
    const buf = Buffer.from(decodedata, 'base64').toString('utf-8');
    const {key} = req.body;
    const task = spawn('python', [path.join(__dirname, 'PYTHON', 'decode.py'), buf, key.toString()]);
    var outpututf8str = "";
    task.stdout.on('data', data => {
        outpututf8str += data.toString();
      });
    task.on('close', (code) => {
      //  console.log(outpututf8str);
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