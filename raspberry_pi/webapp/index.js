var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  let obj = { 1: 'one', 2: 'two', 3: 'three' };
  res.render('index', { title: 'Express',data: obj});
  //res.render('index', { data: obj });
  
});

module.exports = router;

--------------------------------------------------------------------------------------------------------------------------------------------

var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
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
  //res.render('index', { data: obj });
  
});

module.exports = router;
