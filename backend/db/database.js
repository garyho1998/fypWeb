var sqlite3 = require("sqlite3").verbose();
var path = require("path");

let db = new sqlite3.Database(path.join(__dirname, "data.db"), (err) => {
  if (err) {
    console.log(err.message);
    throw err;
  } else {
    console.log("Connected to the SQLite database!");
  }
});

module.exports = db;
