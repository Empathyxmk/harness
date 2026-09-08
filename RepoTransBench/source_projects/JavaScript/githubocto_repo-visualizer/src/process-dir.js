// PATCH: Switch from ESM import to CJS require for Jest compatibility
// import fs from "fs";
// import nodePath from "path";
// import { shouldExcludePath } from "./should-exclude-path";

const fs = require("fs");
const nodePath = require("path");
const { shouldExcludePath } = require("./should-exclude-path");

// See README for high-level overview
async function processDir(dirPath, pathsToIgnore, globsToIgnore) {
  try {
    const stats = fs.statSync(dirPath);
    let node = {
      name: nodePath.basename(dirPath),
      size: stats.size,
    };

    if (stats.isDirectory()) {
      let children = [];
      const files = fs.readdirSync(dirPath);
      for (let file of files) {
        let filePath = nodePath.join(dirPath, file);
        if (shouldExcludePath(filePath, new Set(pathsToIgnore), globsToIgnore)) continue;
        let child = await processDir(filePath, pathsToIgnore, globsToIgnore);
        if (child) children.push(child);
      }
      node.children = children;
    }
    return node;
  } catch (e) {
    return null;
  }
}

module.exports = {
  processDir,
};