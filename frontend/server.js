const express = require("express");
const path = require("path");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 8080;
const API_URL = process.env.API_URL || "http://localhost:8000";

app.use(express.static(__dirname));

app.get("/", (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Workshop App</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <div id="app"></div>
      <script>
        window.API_URL = "${API_URL}";
      </script>
      <script src="app.js"></script>
    </body>
    </html>
  `);
});

app.listen(PORT, () => {
  console.log(`Frontend running at http://localhost:${PORT}`);
});
