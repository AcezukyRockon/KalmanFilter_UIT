const fs = require('fs');
const util = require('util')
const initSqlJs = require('sql.js/dist/sql-wasm.js');
const filebuffer = fs.readFileSync('database.db');

initSqlJs().then(function(SQL){
  // Load the db
  const db = new SQL.Database(filebuffer);
  const contents = db.exec("SELECT * FROM students_name")
  // console.log(contents)
  console.log(util.inspect(contents, false, null, true))
  console.log(contents[0].values[0][1]);
  init_table();
  insert_table("No","Name");
});

function init_table() {
  let table = document.createElement('table');
  let thead = document.createElement('thead');
  let tbody = document.createElement('tbody');

  table.appendChild(thead);
  table.appendChild(tbody);

  // Adding the entire table to the body tag
  document.getElementById('body').appendChild(table);
}

function insert_table(str_num, str_name){
  // Creating and adding data to first row of the table
  let row_1 = document.createElement('tr');
  let heading_1 = document.createElement('th');
  heading_1.innerHTML = str_num;
  let heading_2 = document.createElement('th');
  heading_2.innerHTML = str_name;

  row_1.appendChild(heading_1);
  row_1.appendChild(heading_2);
  thead.appendChild(row_1);
}
