const express = require('express');
const {spawn} = require('child_process');
const path = require('path');
const app = express();

app.use(express.json({limit: '500mb'}));

//afaik the spec for GET says that the body of the sending side should be ignored, so we aren't using it
//not like post is better though, as technically we shouldn't be dumping an entire file back at the client
app.post('/encode', (req, res) => {
    const {genedata} = req.body;
    const {inputdata} = req.body;
    const gbuf = Buffer.from(genedata, 'base64').toString('utf-8');
    const hbuf = Buffer.from(inputdata, 'base64').toString('utf-8');
    const {key} = req.body;
    const {filename} = req.body;
    const fnmstr = Buffer.from(filename, 'base64').toString('utf-8');

    if(!genedata | !inputdata | !key | !filename){
        res.status(400).send()
    }

    const task = spawn('python', [path.join(__dirname, 'PYTHON', 'encode.py'), gbuf, hbuf, key.toString(), fnmstr]);
    var outpututf8str = ""
    task.stdout.on('data', data => {
        outpututf8str += data.toString();
      });

    task.on('close', (code) => {
        if(!outpututf8str){
            res.status(400).send()
        }
        res.send({
            output : `${Buffer.from(outpututf8str).toString('base64')}`
        })
    });
}
);

app.post('/decode', (req, res) => {
    const {decodedata} = req.body;
    const buf = Buffer.from(decodedata, 'base64').toString('utf-8');
    //console.log(buf)
    const {key} = req.body;

    if(!decodedata | !key ){
        res.status(400).send()
    }
    
    const task = spawn('python', [path.join(__dirname, 'PYTHON', 'decode.py'), buf, key.toString()]);
    var outpututf8str = [];
    task.stdout.on('data', data => {
        outpututf8str.push(data.toString())
      });
    task.on('close', (code) => {
        if(!outpututf8str[0] | !outpututf8str[1]){
            res.status(400).send()
        }

        res.status(200).send({
            name : `${Buffer.from(outpututf8str[0]).toString('base64')}`,
            output : `${Buffer.from(outpututf8str[1]).toString('base64')}`
        })
    });


}
);



const port = process.env.PORT || 8080;

app.listen(
    port,
    () => console.log(`listening on ${port}`)
);