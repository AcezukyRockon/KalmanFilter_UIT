var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  let obj = { 1: 'one', 2: 'two', 3: 'three' };
  res.render('index', { title: 'Express',data: obj});
  //res.render('index', { data: obj });
  
});

--------------------------------------------------------------------------------------------------------------------------------------------

module.exports = router;

  var obj = {
   "accounts":{
         "users":[{
            "_id":"5a500vlflg0aslf011ld0a25a5",
            "username":"john",
            "id":"59d25992988fsaj19fe31d7",
            "name":"Test",
            "customer":" John Carew",
         }],
         "applications":[
            {
               "app_id":"5af56pi314-blvinpgn4c95ywyt8j",
               "language":"en"
            }
         ]
      }
   };
  res.render('index', obj.accounts);

--------------------------------------------------------------------------------------------------------------------------------------------

var express = require('express');
var router = express.Router();
const fs = require('fs');
const util = require('util')
const initSqlJs = require('sql.js/dist/sql-wasm.js');
const filebuffer = fs.readFileSync('/home/pi/project/webapp/pythonsqlite.db');

/* GET home page. */
router.get('/', function(req, res, next) {
  initSqlJs().then(function(SQL){
    // Load the db
    var tb = "yes";
    const db = new SQL.Database(filebuffer);
    const contents = db.exec("SELECT * FROM "+tb)
    console.log(util.inspect(contents, false, null, true))
    //console.log(contents[0].values);
    
    var obj = contents;
    res.render('index', obj[0]);
  });
  
  
  //console.log(obj);
  /*var obj = [
  {
    columns: [ 'id', 'd' ],
    values: [
      [ 1, '2022-05-04 15:23:48' ],
      [ 2, '2022-05-04 15:23:50' ],
      [ 3, '2022-05-04 15:24:38' ],
      [ 4, '2022-05-04 15:24:41' ],
      [ 5, '2022-05-04 15:24:43' ],
      [ 6, '2022-05-04 15:24:57' ],
      [ 7, '2022-05-04 15:24:59' ],
      [ 8, '2022-05-04 15:25:01' ]
    ]
  }
];*/

  //res.render('index', obj[0]);
  //res.render('index', { data: obj });
  
});

module.exports = router;

