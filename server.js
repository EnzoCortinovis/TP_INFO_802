var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io') (http);

var soap = require('soap');
//var url = 'http://localhost:6969/?wsdl';
var url = 'https://carlistservice.herokuapp.com/?wsdl';
var args = {num1: 2,num2: 2};

const path = require("path");
const bodyParser = require("body-parser");

app.use(bodyParser.json());

/* soap.createClient(url, function(err, client) {
    client.addition(args, function(err, result) {
        console.log("########################### ADDITION ##############################");
        console.log(result);
    });
}); */
let jason;
soap.createClient(url, function(err, client) {
    client.showCars(function(err, result) {
        console.log("########################### CARS ##############################");
        // let j = JSON.parse(result)
        try {
            jason = JSON.parse(result['showCarsResult'])
        } catch (error) {
            jason = result
        }
        
        console.log(jason);
    });
}); 

// Sockets pour SOAP

app.get('/', function(req, res){
    res.sendFile(__dirname + '/index.html');})
   http.listen(process.env.PORT || 8001, function(){
    console.log('listening on *:8001');
   });  // Pour tester on va sur le navigateur et on entre localhost:3000
       // npm install socket.io
   
   io.on('connection', function(socket){
       console.log('client connecté');
       io.emit('initJson', jason);   
   
   })

// API REST

app.post("/add", (req, res) => {
    const { autonomie, tps_recharge, tps_trajet } = req.body;
    var auto = parseInt(autonomie);
    var recharge = parseInt(tps_recharge);
    var trajet = parseInt(tps_trajet);

    res.send({
      result: trajet + (Math.floor((trajet / auto)) * recharge)
    });
  });