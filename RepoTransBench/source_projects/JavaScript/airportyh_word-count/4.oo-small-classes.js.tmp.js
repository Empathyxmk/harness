"use strict"
const fs = require('fs');

class Tokenizer {
  tokenize(text) {
    return text.split(/[\s.,\/:\n]+/);
  }
}

class FileReader {
  constructor(filepath) {
    this.filepath = filepath;
  }
  read() {
    return fs.readFileSync(this.filepath).toString();
  }
  readWords() {
    return (new Tokenizer).tokenize(this.read());
  }
}

class Tally {
  constructor(words) {
    this.words = words;
    this.tallyUp();
  }
  tallyUp() {
    this.tally = {};
    for (let i = 0; i < this.words.length; i++) {
      let word = this.words[i].toLowerCase();
      this.tally[word] = (this.tally[word] || 0) + 1;
    }
    this.tallyAsArray = [];
    for (let word in this.tally) {
      this.tallyAsArray.push({ word: word, count: this.tally[word] });
    }
    this.tallyAsArray.sort(function(one, other) {
      return other.count - one.count;
    });
    this.tallyAsArray.slice(0, 10);
  }
  getTop10() {
    return this.tallyAsArray.slice(0, 10);
  }
}

class Top10Printer {
  static print(top10) {
    console.log('The top 10 most frequently used:');
    console.log('--------------------------------');
    for (let i = 0; i < top10.length; i++) {
      let rank = i + 1;
      let entry = top10[i];
      console.log(rank + '. ' + entry.word + ': ' + entry.count); 
    }
  }
}

class WordCount {
  static main(filepath = 'words.txt') {
    let words = new FileReader(filepath).readWords();
    let tally = new Tally(words);
    Top10Printer.print(tally.getTop10());
  }
}

module.exports = {
  Tokenizer,
  FileReader,
  Tally,
  Top10Printer,
  WordCount
};