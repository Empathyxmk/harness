"use strict"
const fs = require('fs');

class WordCount {
  constructor(filepath) {
    this.filepath = filepath;
  }
  content() {
    return fs.readFileSync(this.filepath).toString();
  }
  words() {
    return this.content().split(/[\s.,\/:\n]+/);
  }
  tally() {
    let words = this.words();
    let tally = {};
    for (let i = 0; i < words.length; i++) {
      let word = words[i].toLowerCase();
      tally[word] = (tally[word] || 0) + 1;
    }
    return tally;
  }
  top10() {
    let tally = this.tally();
    let tallyAsArray = [];
    for (let word in tally) {
      tallyAsArray.push({ word: word, count: tally[word] });
    }
    tallyAsArray.sort(function(one, other) {
      return other.count - one.count;
    });
    return tallyAsArray.slice(0, 10);
  }
  printTop10() {
    let top10 = this.top10();
    console.log('The top 10 most frequently used:');
    console.log('--------------------------------');
    for (let i = 0; i < top10.length; i++) {
      let rank = i + 1;
      let entry = top10[i];
      console.log(rank + '. ' + entry.word + ': ' + entry.count); 
    }
  }
  static main(filepath = 'words.txt') {
    let tally = new WordCount(filepath);
    tally.printTop10();
  }
}
module.exports = WordCount;