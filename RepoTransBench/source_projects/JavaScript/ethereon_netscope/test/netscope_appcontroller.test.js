// Test for assets/js/netscope.js AppController using Mocha, Chai, Sinon, jsdom

const { expect } = require('chai');
const sinon = require('sinon');
const { JSDOM } = require('jsdom');

describe('AppController', function() {
  let AppController, Renderer, Editor, Notify;
  let dom, window, document, jqueryStub, _, orig$, orig_;
  let loaderCalled, passedNet, cmScriptLoaded;
  let savedOnError, savedWarn, savedErr;

  // Preload fake net object and stubs
  const fakeNet = { name: 'test_network' };

  before(function() {
    // JSDOM with minimal HTML structure required by AppController
    dom = new JSDOM(
      `<html><body>
        <div id="net-container"></div>
        <div id="net-spinner"></div>
        <div id="net-error"><span class="msg"></span></div>
        <div id="net-warning"><span class="msg"></span></div>
        <div id="net-title"></div>
        <svg id="net-svg"></svg>
        <div class="qtip"></div>
      </body></html>`
    );
    window = dom.window;
    document = window.document;
    global.window = window;
    global.document = document;

    // Provide minimal lodash
    _ = {
      isUndefined: (v) => typeof v === 'undefined'
    };
    global._ = _;

    // Provide global $
    const $ = require('jquery')(window); // Use real jQuery on JSDOM window

    // Patch jQuery's .hide(), .show(), .empty(), .remove() with stubs for spying
    ['hide','show','empty'].forEach(function(method) {
      $.fn[method] = function() { this[method + '_called'] = true; return this; };
    });
    $.fn.remove = function() { this['remove_called'] = true; return this; };
    orig$ = global.$;
    global.$ = $;

    // Provide global CodeMirror global for tests
    window.CodeMirror = function() {};

    // Provide fake modules before requiring netscope.js
    // Fake Renderer
    Renderer = sinon.stub().callsFake(function(net, svg) {
      passedNet = net;
      this.net = net;
      this.svg = svg;
    });
    Renderer.prototype = {};
    // Fake Editor
    Editor = sinon.stub().callsFake(function(cb) {
      this.cb = cb;
    });
    // Fake Notify
    Notify = {
      onerror: sinon.stub(),
      onwarning: sinon.stub()
    };

    // Patch require for netscope.js dependencies
    const Module = require('module');
    const originalRequire = Module.prototype.require;
    Module.prototype.require = function(name) {
      if (name.endsWith('renderer.coffee')) return Renderer;
      if (name.endsWith('editor.coffee')) return Editor;
      if (name.endsWith('notify.coffee')) return Notify;
      return originalRequire.apply(this, arguments);
    };
    AppController = require('../assets/js/netscope.js');
    Module.prototype.require = originalRequire; // Restore require
  });

  beforeEach(function() {
    loaderCalled = false;
    passedNet = null;
  });

  describe('constructor', function() {
    it('initializes fields and sets up error handlers', function() {
      const c = new AppController();
      expect(c.inProgress).to.equal(false);
      expect(typeof c.handleError).to.equal('function');
      expect(typeof c.handleWarning).to.equal('function');
      expect(c.$spinner.length).to.equal(1);
      expect(Notify.onerror.called).to.be.true;
      expect(Notify.onwarning.called).to.be.true;
      expect(window.onerror).to.equal(c.handleError);
    });
  });

  describe('startLoading', function() {
    it('triggers hide/shows and calls loader', function(done) {
      const c = new AppController();
      let fakeLoad = function(...args) {
        loaderCalled = true;
        // Last arg is callback
        args[args.length-1](fakeNet);
      };
      c.inProgress = false;
      c.$spinner.hide_called = false;
      c.$netError.hide_called = false;
      c.$spinner.show_called = false;
      c.startLoading(fakeLoad, 1, 2, 3);
      expect(loaderCalled).to.be.true;
      // After async completeLoading, DOM manip occurs:
      setTimeout(()=> {
        expect(c.$spinner.hide_called).to.be.true;
        expect($('.qtip').get(0).remove_called).to.equal(true);
        done();
      }, 10);
    });

    it('exits early if already in progress', function() {
      const c = new AppController();
      c.inProgress = true;
      const loader = sinon.spy();
      c.startLoading(loader); // Should NOT call loader if inProgress
      expect(loader.called).to.be.false;
    });
  });

  describe('completeLoading', function() {
    it('shows network and calls Renderer', function() {
      const c = new AppController();
      c.$spinner.hide_called = false;
      c.$netBox.show_called = false;
      c.svg = '#net-svg';
      $(c.svg).empty_called = false;
      $('.qtip').remove_called = false;
      c.completeLoading(fakeNet);
      expect(c.$spinner.hide_called).to.be.true;
      expect($('#net-title').html()).to.contain('test network');
      expect(c.$netBox.show_called).to.be.true;
      expect($(c.svg).empty_called).to.be.true;
      expect($('.qtip').remove_called).to.be.true;
      expect(Renderer.called).to.be.true;
      expect(passedNet).to.equal(fakeNet);
      expect(c.inProgress).to.be.false;
    });
  });

  describe('makeLoader', function() {
    it('wraps a loader so it calls startLoading', function() {
      const c = new AppController();
      sinon.spy(c, 'startLoading');
      function demoLoader() {}
      const wrapped = c.makeLoader(demoLoader);
      wrapped(1,2,3);
      expect(c.startLoading.calledWith(demoLoader,1,2,3)).to.be.true;
    });
  });

  describe('showEditor', function() {
    it('loads script if no CodeMirror, instantiates Editor after load', function(done) {
      const c = new AppController();
      delete window.CodeMirror;
      let getScriptStub = sinon.stub(global.$, 'getScript').callsFake(function(src, cb) {
        // Simulate loading CM, then call cb:
        window.CodeMirror = function() {};
        setTimeout(()=>{
          cb();
          expect(Editor.called).to.be.true;
          $.getScript.restore();
          done();
        },5);
      });
      c.showEditor({ load: function(){} });
    });

    it('does nothing if CodeMirror exists', function() {
      const c = new AppController();
      window.CodeMirror = function(){ return true; };
      sinon.spy(global.$, 'getScript');
      c.showEditor({ load: function(){} });
      expect($.getScript.called).to.be.false;
      $.getScript.restore();
    });
  });

  describe('handleError', function() {
    it('shows error message and disables spinner and sets inProgress false', function() {
      const c = new AppController();
      c.$spinner.hide_called = false;
      c.$netError.show_called = false;
      let res = c.handleError('msg', 'file', 42, 5, null);
      expect(c.$spinner.hide_called).to.be.true;
      expect(c.$netError.show_called).to.be.true;
      expect(c.inProgress).to.be.false;
      expect($('.msg', c.$netError).html()).to.be.equal('msg');
    });

    it('shows source location if error with line & col', function() {
      const c = new AppController();
      c.$spinner.hide_called = false;
      c.$netError.show_called = false;
      let e = { line: 3, column: 2, message: 'oops', toString:()=> 'o' };
      c.handleError('msg','somewhere',3,2,e);
      expect($('.msg', c.$netError).html()).to.contain('Line 3, Column 2: oops');
    });
  });

  describe('handleWarning', function() {
    it('shows warning message and makes warning visible', function() {
      const c = new AppController();
      c.$netWarn.show_called = false;
      c.handleWarning('test warning!');
      expect($('.msg', c.$netWarn).html()).to.equal('test warning!');
      expect(c.$netWarn.show_called).to.be.true;
    });
  });
});