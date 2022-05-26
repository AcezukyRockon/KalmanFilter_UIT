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

working--------------------------------------------------------------------------------------------------------------------------------------------

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
    console.log(req.query.title);
    var tb = req.query.title;
    const db = new SQL.Database(filebuffer);
    
    if (tb == undefined) {
      console.log("nothing to retrieve");
      const list_tb = db.exec("SELECT name FROM sqlite_schema WHERE type='table';")
      res.render('index-notable',{title : 'No table chosen', list_tb: list_tb[0]});
    }
    else {
      const list_tb = db.exec("SELECT name FROM sqlite_schema WHERE type='table';")
      const contents = db.exec("SELECT * FROM "+tb)
      console.log(util.inspect(contents, false, null, true))
      //console.log(contents[0].values);
      
      var obj = contents;
      res.render('index', {title : tb, list_tb: list_tb[0], data: obj[0]});
    }

  });
});

module.exports = router;
