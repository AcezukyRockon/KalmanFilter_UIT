var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  let obj = { 1: 'one', 2: 'two', 3: 'three' };
  res.render('index', { title: 'Express',data: obj});
  //res.render('index', { data: obj });
  
});

module.exports = router;
