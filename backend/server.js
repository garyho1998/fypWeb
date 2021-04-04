const express = require("express");
const bodyParser = require("body-parser");
const path = require("path");
const app = express();
const port = process.env.PORT || 8080;
const db = require("./db/database");
const cors = require("cors");

app.use(express.static(path.join(__dirname, "build")));

app.use(cors());

app.get("/health", function (req, res) {
  return res.send("ok");
});

app.get("/", function (req, res) {
  res.sendFile(path.join(__dirname, "build", "index.html"));
});

// Get product info API
app.get("/it_solution", function (req, res) {
  db.all("SELECT * FROM it_solution", (err, rows) => {
    if (err) {
      res.status(400).json({ error: err.message });
      return;
    }
    res.status(200).json({ data: rows });
  });
});

app.get("/it_solution_one", function (req, res) {
  data = [req.query.id];
  sql = `SELECT * FROM it_solution where it_solution."Reference Code" == ?`;
  db.all(sql, data, (err, rows) => {
    if (err) {
      res.status(400).json({ error: err.message });
      return;
    }
    res.status(200).json({ data: rows[0] });
  });
});

app.get("/businessMatch", function (req, res) {
  sql = `Select business_need.*  from match_data, business_need 
    where business_need."Reference Code" == match_data."Business Reference Code" Group by business_need."Reference Code"`;
  db.all(sql, (err, rows) => {
    if (err) {
      res.status(400).json({ error: err.message });
      return;
    }
    res.status(200).json({ data: rows });
  });
});

app.get("/newbusinessMatch", function (req, res) {
  try {
    arg1 = req.query.paragraph;
    console.log("arg1", arg1);
    var spawn = require("child_process").spawn,
      pythonProcess = spawn("python", [
        __dirname + "/dataprocessing/process_business_need_large_roberta.py",
        arg1,
      ]),
      json = "";

    pythonProcess.stdout.on("data", (data) => {
      json += data;
    });
    pythonProcess.stderr.on("close", () => {
      console.log("close");
      res.status(200).json({ data: JSON.parse(json) });
    });
  } catch (e) {
    console.log("catch error", str(e));
  }
});

app.get("/solutionMatch", function (req, res) {
  data = [req.query.id];
  sql = `Select match_data.*, business_need."Title (Eng)" as "Business Title", py.year as "Year", py."Sentence Output", py."Answer",  it_solution."Application Areas", it_solution."Solution Description"
  from match_data, business_need, project_and_year as py, it_solution 
  where match_data."Business Reference Code" == ? and business_need."Reference Code" == match_data."Business Reference Code" 
  and py."Reference Code" == match_data."Reference Code"
  and py."Reference Code" == it_solution."Reference Code"`;
  db.all(sql, data, (err, rows) => {
    if (err) {
      res.status(400).json({ error: err.message });
      return;
    }
    res.status(200).json({ data: rows });
  });
});
app.listen(port, () => {
  console.log(`Start listening on port ${port}...`);
});

module.exports = { app };
