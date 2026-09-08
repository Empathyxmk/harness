// Public tests for assets/js/netscope.js AppController using Mocha, Chai, Sinon, jsdom
// Test values are different from those in the original test, but logic is preserved

const { expect } = require('chai');
const sinon = require('sinon');
const { JSDOM } = require('jsdom');

describe('AppController (public)', function() {
  let AppController, Renderer, Editor, Notify;
  let dom, window, document, jqueryStub, _, orig$, orig_;
  let loaderCalled, passedNet, cmScriptLoaded;
  let savedOnError, savedWarn, savedErr;

  // Use a different fake net object
  const fakeNetPublic = { name: 'public_network_example' };

  before(function() {
    // JSDOM with minimal HTML structure, use different ids to still support code
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
    const $ = require('jquery')(window);

    ['hide','show','empty'].forEach(function(method) {
      $.fn[method] = function() { this[method + '_called'] = true; return this; };
    });
    $.fn.remove = function() { this['remove_called'] = true; return this; };
    orig$ = global.$;
    global.$ = $;

    // Provide global CodeMirror global for tests
    window.CodeMirror = function() {};

    // Provide fake modules before requiring netscope.js
    Renderer = sinon.stub().callsFake(function(net, svg) {
      passedNet = net;
      this.net = net;
      this.svg = svg;
    });
    Renderer.prototype = {};
    Editor = sinon.stub().callsFake(function(cb) {
      this.cb = cb;
    });
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
    it('initializes fields and sets up error handlers (public)', function() {
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
    it('triggers hide/shows and calls loader (public)', function(done) {
      const c = new AppController();
      let fakeLoad = function(...args) {
        loaderCalled = true;
        args[args.length-1](fakeNetPublic); // Pass different net
      };
      c.inProgress = false;
      c.$spinner.hide_called = false;
      c.$netError.hide_called = false;
      c.$spinner.show_called = false;
      c.startLoading(fakeLoad, 500, 800); // Different loader params
      expect(loaderCalled).to.be.true;
      // After async completeLoading, DOM manip occurs:
      setTimeout(()=> {
        expect(c.$spinner.hide_called).to.be.true;
        expect($('.qtip').get(0).remove_called).to.equal(true);
        done();
      }, 10);
    });

    it('exits early if already in progress (public)', function() {
      const c = new AppController();
      c.inProgress = true;
      const loader = sinon.spy();
      c.startLoading(loader);
      expect(loader.called).to.be.false;
    });
  });

  describe('completeLoading', function() {
    it('shows network and calls Renderer (public)', function() {
      const c = new AppController();
      c.$spinner.hide_called = false;
      c.$netBox.show_called = false;
      c.svg = '#net-svg';
      $(c.svg).empty_called = false;
      $('.qtip').remove_called = false;
      c.completeLoading(fakeNetPublic);
      expect(c.$spinner.hide_called).to.be.true;
      expect($('#net-title').html()).to.contain('public network example'); // underscores replaced w/ space
      expect(c.$netBox.show_called).to.be.true;
      expect($(c.svg).empty_called).to.be.true;
      expect($('.qtip').remove_called).to.be.true;
      expect(Renderer.called).to.be.true;
      expect(passedNet).to.equal(fakeNetPublic);
      expect(c.inProgress).to.be.false;
    });
  });

  describe('makeLoader', function() {
    it('wraps a loader so it calls startLoading (public)', function() {
      const c = new AppController();
      sinon.spy(c, 'startLoading');
      function demoLoaderPub() {}
      const wrapped = c.makeLoader(demoLoaderPub);
      wrapped('a','b','c');
      expect(c.startLoading.calledWith(demoLoaderPub, 'a','b','c')).to.be.true;
    });
  });

  describe('showEditor', function() {
    it('loads script if no CodeMirror, instantiates Editor after load (public)', function(done) {
      const c = new AppController();
      delete window.CodeMirror;
      let getScriptStub = sinon.stub(global.$, 'getScript').callsFake(function(src, cb) {
        window.CodeMirror = function() {}; // simulate CM loaded
        setTimeout(()=>{
          cb();
          expect(Editor.called).to.be.true;
          $.getScript.restore();
          done();
        },4);
      });
      c.showEditor({ load: function(){} });
    });

    it('does nothing if CodeMirror exists (public)', function() {
      const c = new AppController();
      window.CodeMirror = function(){ return 42; };
      sinon.spy(global.$, 'getScript');
      c.showEditor({
        load: function(){}
      });
      expect(global.$.getScript.called).to.be.false;
      global.$.getScript.restore();
    });
  });
});