const proxyquire = require('proxyquire').noCallThru();
const sinon = require('sinon');
const { expect } = require('chai');
const mockFs = require('mock-fs');

describe('Gruntfile.js (Public Tests)', () => {
  let fsStub, globStub, _mock, languagesStub, gruntStub, registeredTasks;

  beforeEach(() => {
    // Reset stubs and mocks before every test
    registeredTasks = {};
    fsStub = {
      writeFileSync: sinon.spy()
    };
    globStub = {
      sync: sinon.stub()
    };
    // Underscore
    _mock = {
      each: (arr, cb) => arr.forEach(cb),
      sortBy: (arr, iter) => arr.slice().sort((a, b) => {
        let aVal = iter(a), bVal = iter(b);
        if (aVal < bVal) return -1;
        if (aVal > bVal) return 1;
        return 0;
      }),
      map: (arr, cb) => arr.map(cb)
    };
    languagesStub = {
      getLanguageInfo: (code) => ({ name: { "de": "German", "it": "Italian", "zz": "Unknownish" }[code] || code })
    };
    gruntStub = {
      file: {
        readJSON: sinon.stub().returns({ license: 'Apache-2.0' }),
        read: sinon.stub()
      },
      initConfig: sinon.spy(),
      loadNpmTasks: sinon.spy(),
      registerTask: (name, fn) => {
        registeredTasks[name] = fn;
      }
    };
  });

  afterEach(() => {
    mockFs.restore();
  });

  it('registers stopwordsToJson and stopwordsDocs tasks with different languages', () => {
    // Use different language files for the public test
    globStub.sync.returns([
      'src/smart/de.txt',
      'src/smart/it.txt'
    ]);

    gruntStub.file.read.withArgs('src/smart/de.txt').returns('eins\nzwei\ndrei');
    gruntStub.file.read.withArgs('src/smart/it.txt').returns('uno\ndue\ntre');

    // Proxyquire Gruntfile.js with stubs
    proxyquire('../Gruntfile.js', {
      fs: fsStub,
      glob: globStub,
      underscore: _mock,
      languages: languagesStub
    })(gruntStub);

    // Test 'stopwordsToJson'
    expect(registeredTasks).to.have.property('stopwordsToJson');
    registeredTasks['stopwordsToJson']();

    // Should write two dist jsons and stopwords-all.json
    expect(fsStub.writeFileSync.callCount).to.equal(3);
    expect(fsStub.writeFileSync.firstCall.args[0]).to.contain('dist/de.json');
    expect(fsStub.writeFileSync.secondCall.args[0]).to.contain('dist/it.json');
    expect(fsStub.writeFileSync.thirdCall.args[0]).to.equal('stopwords-all.json');
    let itJson = JSON.parse(fsStub.writeFileSync.secondCall.args[1]);
    expect(itJson).to.include.members(['uno','due','tre']);

    // Test 'stopwordsDocs'
    registeredTasks['stopwordsDocs']();
    expect(fsStub.writeFileSync.callCount).to.be.at.least(4);
    expect(fsStub.writeFileSync.lastCall.args[0]).to.equal('docs/supported-languages.md');
    expect(fsStub.writeFileSync.lastCall.args[1]).to.include('Language | Stopword count | Filename');
    expect(fsStub.writeFileSync.lastCall.args[1]).to.include('German');
    expect(fsStub.writeFileSync.lastCall.args[1]).to.include('Italian');
  });

  it('wordsInFile ignores empty and comment lines with new data', () => {
    let called = false;
    proxyquire('../Gruntfile.js', {
      fs: fsStub,
      glob: globStub,
      underscore: {
        ..._mock,
        each: (arr, fn) => {
          if (arr[0] && arr[0].includes('#ignore')) called = true;
          arr.forEach(fn);
        }
      },
      languages: languagesStub
    })(gruntStub);
    globStub.sync.returns(['src/smart/de.txt']);
    gruntStub.file.read.withArgs('src/smart/de.txt').returns('das\n#ignore\n\nund');
    registeredTasks['stopwordsToJson']();
    expect(called).to.be.true;
    let deJson = JSON.parse(fsStub.writeFileSync.firstCall.args[1]);
    expect(deJson).to.include('das');
    expect(deJson).to.include('und');
    expect(deJson).to.not.include('#ignore');
    expect(deJson).to.not.include('');
  });

  it('getStopwords memoizes and sorts with different file', () => {
    globStub.sync.returns(['src/smart/it.txt']);
    gruntStub.file.read.withArgs('src/smart/it.txt').returns('beta\nalpha\ngamma');
    let firstList, secondList;
    proxyquire('../Gruntfile.js', {
      fs: fsStub,
      glob: globStub,
      underscore: _mock,
      languages: languagesStub
    })(gruntStub);

    // Call stopwordsDocs twice (which triggers getStopwords)
    registeredTasks['stopwordsDocs']();
    firstList = JSON.parse(fsStub.writeFileSync.lastCall.args[1]);
    registeredTasks['stopwordsDocs']();
    secondList = JSON.parse(fsStub.writeFileSync.lastCall.args[1]);
    expect(firstList).to.deep.equal(secondList);
    // Should be sorted alphabetically
    expect(firstList).to.include('alpha');
    expect(firstList.indexOf('alpha')).to.be.below(firstList.indexOf('beta'));
  });

  it('handles files with duplicate words per language (public data)', () => {
    globStub.sync.returns(['src/smart/de.txt']);
    gruntStub.file.read.withArgs('src/smart/de.txt').returns('foo\nbar\nfoo\nbaz\nbar');
    proxyquire('../Gruntfile.js', {
      fs: fsStub,
      glob: globStub,
      underscore: _mock,
      languages: languagesStub
    })(gruntStub);
    registeredTasks['stopwordsToJson']();
    let deJson = JSON.parse(fsStub.writeFileSync.firstCall.args[1]);
    expect(deJson).to.include('foo');
    expect(deJson).to.include('bar');
    expect(deJson).to.include('baz');
    expect(deJson.filter(w => w==='foo').length).to.equal(1);
    expect(deJson.filter(w => w==='bar').length).to.equal(1);
  });

  it('stopwordsDocs handles unknown language code gracefully (public)', () => {
    globStub.sync.returns(['src/smart/zz.txt']);
    gruntStub.file.read.withArgs('src/smart/zz.txt').returns('apple\norange');
    proxyquire('../Gruntfile.js', {
      fs: fsStub,
      glob: globStub,
      underscore: _mock,
      languages: {
        getLanguageInfo: () => ({ name: 'Unknownish' })
      }
    })(gruntStub);
    registeredTasks['stopwordsDocs']();
    expect(fsStub.writeFileSync.lastCall.args[1]).to.include('Unknownish');
    expect(fsStub.writeFileSync.lastCall.args[1]).to.include('zz.json');
  });

});