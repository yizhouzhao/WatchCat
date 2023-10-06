import express from "express";
import logger from "morgan";
import * as path from "path";

import { errorHandler, errorNotFoundHandler } from "./middlewares/errorHandler";

// Routes
import { index } from "./routes/index";
// Create Express server
export const app = express();

//debug
app.get('test', (req, res) => {
    console.log('Received req:' + req.url + ' from ' + req.ip + ' at ' + new Date().toISOString().replace(/T/, ' ').replace(/\..+/, ''));
    console.log("req.headers: " + JSON.stringify(req.headers.authorization));
    res.send('Connection successful! Your Express server is up and running.');
  });
  

// Express configuration
app.set("port", process.env.PORT || 3000);
app.set("views", path.join(__dirname, "../views"));
app.set("view engine", "pug");

app.use(logger("dev"));

app.use(express.static(path.join(__dirname, "../public")));
app.use("/", index);

app.use(errorNotFoundHandler);
app.use(errorHandler);

