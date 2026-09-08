(function (rlite) {
  // Public test cases for Rlite router -- same logic as original, but different input/output values.

  function noop() {}

  describe('Rlite (public test cases)', function () {

    it('Does not put hash values in query (public)', function () {
      const route = rlite(noop, {alpha: ({id}) => expect(id).toEqual('42')});

      route('alpha?id=42#sectionfoo');
    });

    it('Has empty params for parameterless routes (public)', function () {
      const route = rlite(noop, {
        beta: (params) => expect(Object.keys(params).length).toEqual(0)
      });

      route('beta');
    });

    it('Returns the result of the route (public)', function () {
      const route = rlite(noop, {
        greet: () => 'Hola Alice',
        farewell: () => 'Adieu Bob',
      });

      expect(route('greet')).toEqual('Hola Alice');
      expect(route('farewell')).toEqual('Adieu Bob');
    });

    it('Handles leading/trailing slashes and 404s (public)', function () {
      const route = rlite(() => 'NopePublic!', {
        delta: () => 'YepPublic!'
      });

      expect(route('/delta/')).toEqual('YepPublic!');
      expect(route('delta/')).toEqual('YepPublic!');
      expect(route('/delta')).toEqual('YepPublic!');
      expect(route('delta')).toEqual('YepPublic!');
      expect(route('somethingelse')).toEqual('NopePublic!');
    });

    it('Handles deep conflicting routes (public)', function () {
      const route = rlite(() => 'not:found', {
        'baz/:qux/quux': ({qux}) => `Qux=${qux}`,
        'baz/:qux/:foo': ({qux, foo}) => `Qux=${qux}, Foo=${foo}`,
        'baz/qux/bar': () => 'FoundBar',
      });

      expect(route('/baz/qux/quux/')).toEqual('Qux=qux');
      expect(route('/baz/y/z/')).toEqual('Qux=y, Foo=z');
      expect(route('/baz/qux/bar/')).toEqual('FoundBar');
    });

    it('Handles route params (public)', function() {
      const route = rlite(noop, {
        'shout/:word': ({word}) => expect(word).toEqual('example')
      });

      route('shout/example');
    });

    it('Handles different cases (public)', function() {
      let count = 0;
      const route = rlite(noop, {
        'Shout/:word': ({word}) => {
          expect(word).toEqual('example');
          ++count;
        },
        'whisper/:phrase': ({phrase}) => {
          expect(phrase).toEqual('hi');
          ++count;
        },
        'Yell/:Phrase/:Other': ({Phrase, Other}) => {
          expect(Phrase).toEqual('Foo');
          expect(Other).toEqual('Bar');
          ++count;
        }
      });

      route('shout/example');
      route('whisper/hi');
      route('yell/Foo/Bar');
      expect(count).toBe(3);
    });

    it('Passes the argument and url through (public)', function() {
      const route = rlite(noop, {
        'call/:who': ({who}, arg, url) => {
          expect(arg).toEqual('ArgTest');
          expect(who).toEqual('Bob');
          expect(url).toEqual('call/Bob');
        }
      });

      route('call/Bob', 'ArgTest');
    });

    it('Matches root routes correctly (public)', function() {
      const route = rlite(noop, {
        'foo/:value/new': () => {throw new Error('New called');},
        'foo/:value': ({value}) => expect(value).toEqual('baz'),
        'foo/:value/edit': () => {throw new Error('Edit called');},
      });

      route('foo/baz');
    });

    it('Understands specificity (public)', function() {
      const route = rlite(noop, {
        'foo/lisa': (_1, _2, url) => expect(url).toEqual('foo/lisa'),
        'foo/:person': () => {throw new Error('Person called')},
        'foo/sam': (_1, _2, url) => expect(url).toEqual('foo/sam'),
      });

      route('foo/lisa');
      route('foo/sam');
    });

    it('Handles complex routes (public)', function() {
      const route = rlite(noop, {
        'address/:city/new': () => {throw new Error('New called');},
        'address/:city': () => {throw new Error('City called');},
        'address/:city/state/:state': ({city, state}) => {
          expect(city).toEqual('springfield');
          expect(state).toEqual('illinois');
        }
      });

      route('address/springfield/state/illinois');
    });

    it('Overrides params with query string values (public)', function() {
      const route = rlite(noop, {
        'foo/:bar/new': () => {throw new Error('New called');},
        'foo/:bar': () => {throw new Error('Bar called');},
        'foo/:bar/second/:baz': function({bar, baz}) {
          expect(bar).toEqual('cheese');
          expect(baz).toEqual('lettuce');
          return bar + ' ' + baz;
        }
      });

      expect(route('foo/original/second/mayon/?baz=lettuce&bar=cheese')).toEqual('cheese lettuce');
    });

    it('Handles not founds (public)', function() {
      const route = rlite(() => 'notfound', {
        'bar/:baz': () => {throw new Error('baz called');}
      });

      expect(route('bar?bogus=val')).toEqual('notfound');
    });

    it('Handles default urls (public)', function() {
      const route = rlite(noop, {
        '': () => 'HOMEPUB'
      });

      expect(route('')).toEqual('HOMEPUB');
    });

    it('Handles multiple params in a row (public)', function() {
      const route = rlite(noop, {
        'foo/:alpha/:beta': ({alpha, beta}) => {
          expect(alpha).toEqual('param1');
          expect(beta).toEqual('param2');
        }
      });

      route('foo/param1/param2');
    });

    it('Handles trailing slash with query (public)', function() {
      const route = rlite(noop, {
        'bar': ({item}) => {
          expect(item).toEqual('bike');
          return 'YesQuery';
        }
      });

      expect(route('bar/?item=bike')).toEqual('YesQuery');
    });

    it('Handles leading slashes in defs (public)', function() {
      const route = rlite(noop, {
        '/zigzag': () => 'GOTPUBLIC'
      });

      expect(route('zigzag')).toEqual('GOTPUBLIC');
    });

    // Note: To keep test set substantial, add similar coverage for wildcards if needed.
    it('Handles wildcard routes (public)', function() {
      const route = rlite(() => 'NO MATCH', {
        '/people/:who/biz': ({who}) => `Hello ${who}`,
        '/people/*who': ({who}) => `Wildcard ${who}`,
        '/fruit/:kind/box': ({kind}) => `FruitBox ${kind}`,
        '/fruit/*what': ({what}) => `AllFruit ${what}`
      });

      expect(route('people/mike/biz')).toEqual('Hello mike');
      expect(route('people/charlie/zoo')).toEqual('Wildcard charlie/zoo');
      expect(route('fruit/apple/box')).toEqual('FruitBox apple');
      expect(route('fruit/banana/blah')).toEqual('AllFruit banana/blah');
      expect(route('unknown/blah')).toEqual('NO MATCH');
    });

  });
}(typeof require === 'function'
    ? require('../rlite')
    : this.Rlite
));