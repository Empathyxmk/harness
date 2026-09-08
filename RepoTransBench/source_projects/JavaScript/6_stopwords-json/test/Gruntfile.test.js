const proxyquire = require('proxyquire').noCallThru();
const sinon = require('sinon');
const { expect } = require('chai');
const mockFs = require('mock-fs');

describe('Gruntfile.js', () => {
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
      getLanguageInfo: (code) => ({ name: { "en": "English", "es": "Spanish", "fr": "French", "xx": "Unknown" }[code] || code })
    };
    gruntStub = {
      file: {
        readJSON: sinon.stub().returns({ license: 'MIT' }),
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

  it('registers stopwordsToJson and stopwordsDocs tasks', () => {
    // fake files for glob
    globStub.sync.returns([
      'src/smart/en.txt',
      'src/smart/es.txt'
    ]);

    gruntStub.file.read.withArgs('src/smart/en.txt').returns('foo\nbar\nbaz');
    gruntStub.file.read.withArgs('src/smart/es.txt').returns('uno\ndos\ntres');

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
    expect(fsStub.writeFileSync.firstCall.args[0]).to.contain('dist/en.json');
    expect(fsStub.writeFileSync.secondCall.args[0]).to.contain('dist/es.json');
    expect(fsStub.writeFileSync.thirdCall.args[0]).to.equal('stopwords-all.json');
    let esJson = JSON.parse(fsStub.writeFileSync.secondCall.args[1]);
    expect(esJson).to.include.members(['uno','dos','tres']);

    // Test 'stopwordsDocs'
    registeredTasks['stopwordsDocs']();
    expect(fsStub.writeFileSync.callCount).to.be.at.least(4);
    expect(fsStub.writeFileSync.lastCall.args[0]).to.equal('docs/supported-languages.md');
    expect(fsStub.writeFileSync.lastCall.args[1]).to.include('Language | Stopword count | Filename');
    expect(fsStub.writeFileSync.lastCall.args[1]).to.include('English');
    expect(fsStub.writeFileSync.lastCall.args[1]).to.include('Spanish');
  });

  it('wordsInFile ignores empty and comment lines', () => {
    let called = false;
    proxyquire('../Gruntfile.js', {
      fs: fsStub,
      glob: globStub,
      underscore: {
        ..._mock,
        each: (arr, fn) => {
          if (arr[0] && arr[0].includes('#')) called = true;
          arr.forEach(fn);
        }
      },
      languages: languagesStub
    })(gruntStub);
    // indirectly tested via stopwordsToJson
    globStub.sync.returns(['src/smart/en.txt']);
    gruntStub.file.read.withArgs('src/smart/en.txt').returns('foo\n#bar\n\nbaz');
    registeredTasks['stopwordsToJson']();
    expect(called).to.be.true;
    let enJson = JSON.parse(fsStub.writeFileSync.firstCall.args[1]);
    expect(enJson).to.include('foo');
    expect(enJson).to.include('baz');
    expect(enJson).to.not.include('#bar');
    expect(enJson).to.not.include('');
  });

  it('getStopwords memoizes and sorts', () => {
    globStub.sync.returns(['src/smart/en.txt']);
    gruntStub.file.read.withArgs('src/smart/en.txt').returns('bbb\naaa\nccc');
    let capturedStopwords1, capturedStopwords2;
    proxyquire('../Gruntfile.js', {
      fs: fsStub,
      glob: globStub,
      underscore: _mock,
      languages: languagesStub
    })(gruntStub);

    // Call stopwordsDocs twice (which triggers getStopwords)
    registeredTasks['stopwordsDocs']();
    capturedStopwords1 = JSON.parse(fsStub.writeFileSync.lastCall.args[1]);
    registeredTasks['stopwordsDocs']();
    capturedStopwords2 = JSON.parse(fsStub.writeFileSync.lastCall.args[1]);
    expect(capturedStopwords1).to.deep.equal(capturedStopwords2);
    // Should be sorted alphabetically
    expect(capturedStopwords1).to.include('aaa');
    expect(capturedStopwords1.indexOf('aaa')).to.be.below(capturedStopwords1.indexOf('bbb'));
  });

  it('handles files with duplicate words per language', () => {
    globStub.sync.returns(['src/smart/en.txt']);
    gruntStub.file.read.withArgs('src/smart/en.txt').returns('foo\nfoo\nbar\nbaz\nbar');
    proxyquire('../Gruntfile.js', {
      fs: fsStub,
      glob: globStub,
      underscore: _mock,
      languages: languagesStub
    })(gruntStub);
    registeredTasks['stopwordsToJson']();
    let enJson = JSON.parse(fsStub.writeFileSync.firstCall.args[1]);
    expect(enJson).to.include('foo');
    expect(enJson).to.include('bar');
    expect(enJson).to.include('baz');
    expect(enJson.filter(w => w==='foo').length).to.equal(1);
    expect(enJson.filter(w => w==='bar').length).to.equal(1);
  });

  it('stopwordsDocs handles unknown language code gracefully', () => {
    globStub.sync.returns(['src/smart/xx.txt']);
    gruntStub.file.read.withArgs('src/smart/xx.txt').returns('hello\nworld');
    proxyquire('../Gruntfile.js', {
      fs: fsStub,
      glob: globStub,
      underscore: _mock,
      languages: {
        getLanguageInfo: () => ({ name: 'Unknown' })
      }
    })(gruntStub);
    registeredTasks['stopwordsDocs']();
    expect(fsStub.writeFileSync.lastCall.args[1]).to.include('Unknown');
  });

  it('default task registers all sub-tasks', () => {
    proxyquire('../Gruntfile.js', {
      fs: fsStub,
      glob: globStub,
      underscore: _mock,
      languages: languagesStub
    })(gruntStub);

    expect(gruntStub.initConfig.called).to.be.true;
    expect(gruntStub.loadNpmTasks.calledWith('grunt-readme')).to.be.true;
    expect(Object.keys(registeredTasks)).to.include.members(['stopwordsToJson', 'stopwordsDocs', 'default']);
  });
});