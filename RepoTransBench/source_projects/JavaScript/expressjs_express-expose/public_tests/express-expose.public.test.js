var express = require('express');
var expose = require('../');
var assert = require('assert');
var should = require('should');
var vm = require('vm');
var request = require('supertest');

describe('expose (public tests)', function() {

  it('test app.expose(name) with alternative data', function() {

    var app = express();
    app = expose(app);
    app.expose({ alpha: 10, beta: 20, gamma: 30 });
    app.expose({ subtitle: 'Your Portal' }, 'app.options');
    app.expose({ multiply: function(a, b){ return a * b; } }, 'utils');
    app.expose({ es: 'Español' }, 'langs', 'langs');

    var js = app.exposed();
    var scope = {};

    scope.window = scope;
    vm.runInNewContext(js, scope);
    scope.app.alpha.should.equal(10);
    scope.app.beta.should.equal(20);
    scope.app.gamma.should.equal(30);

    scope.app.options.subtitle.should.equal('Your Portal');
    scope.utils.multiply(2,4).should.equal(8);

    js = app.exposed('langs');
    scope = {};

    scope.window = scope;
    vm.runInNewContext(js, scope);
    scope.should.not.have.property('express');
    scope.langs.es.should.equal('Español');

  });

  it('test app.expose(str) with different variable names', function() {

    var app = express();
    app = expose(app);

    app
      .expose('var product = { name: "widget" };')
      .expose('var locale = "fr";');

    var js = app.exposed();
    var scope = {};

    vm.runInNewContext(js, scope);
    scope.locale.should.equal('fr');
    scope.product.name.should.equal('widget');

  });

  it('test app.expose(str, null, scope) with swapped names', function() {

    var app = express();
    app = expose(app);

    app
      .expose('var person = { name: "alex" };', 'head')
      .expose('var region = "eu";');

    var js = app.exposed();
    var scope = {};

    vm.runInNewContext(js, scope);
    scope.region.should.equal('eu');
    scope.should.not.have.property('person');

    js = app.exposed('head');
    vm.runInNewContext(js, scope = {});
    scope.should.not.have.property('region');
    scope.person.name.should.equal('alex');

  });

  it('test app.expose(fn) self-calling with new data', function() {

    var app = express();
    app = expose(app);

    app.expose('var bar;');
    app.expose(function(){
      this.bar = 'baz';
      var hidden = 'hidden';
    });

    app.expose('var city;', 'leg');
    app.expose(function() {
      this.city = 'oslo';
    }, 'leg');

    var js = app.exposed();
    var scope = {};

    vm.runInNewContext(js, scope);
    scope.bar.should.equal('baz');
    scope.should.not.have.property('hidden');
    scope.should.not.have.property('city');

    js = app.exposed('leg');
    scope = {};
    scope.window = scope;
    vm.runInNewContext(js, scope);
    scope.should.not.have.property('bar');
    scope.city.should.equal('oslo');

  });

  it('test app.expose(fn) named function with different math', function() {

    var app = express();
    app = expose(app);

    app.expose(function multiply(a, b){
      return a * b;
    });

    app.expose(function divide(a, b){
      return a / b;
    }, 'leg');

    var js = app.exposed();
    var scope = {};

    scope.window = scope;
    vm.runInNewContext(js, scope);
    scope.multiply(2,5).should.equal(10);
    scope.should.not.have.property('divide');

    js = app.exposed('leg');
    scope = {};

    scope.window = scope;
    vm.runInNewContext(js, scope);
    scope.divide(10,2).should.equal(5);
    scope.should.not.have.property('multiply');

  });

  it('test res.expose(str) with alternate fields', function(done) {

    var app = express();
    app = expose(app);
    app.set('view engine', 'jade');
    app.set('views', __dirname + '/views');

    app.expose('var settings = { theme: "dark" };');
    app.expose('settings.version = 2;');

    app.get('/', function(req, res) {
      res.expose('var lang = "es";');
      res.expose('var country = "es";');
      res.render('index');
    });

    request(app)
      .get('/')
      .end(function(err, res) {
        if (err) throw err;

        var scope = {};
        vm.runInNewContext(res.text, scope);
        scope.settings.theme.should.equal('dark');
        scope.settings.version.should.equal(2);
        scope.country.should.equal('es');
        scope.lang.should.equal('es');
        done();
      });

  });

});