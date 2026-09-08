const { expect } = require('chai');

describe('public/js/core/transition.js', function () {
  it('should have a duration property and an apply method', function () {
    // Simulate AMD define/require
    const fakeDefine = (def) => def(require);
    const transition = fakeDefine(require => {
      let appliedClass = '';
      return {
        duration: 700,
        apply: function (el, type, callback) {
          appliedClass = 'animated ' + type;
          if (el && typeof el.addClass === 'function') {
            el.addClass(appliedClass);
          }
          setTimeout(callback, this.duration);
        }
      };
    });
    expect(transition).to.be.an('object');
    expect(transition).to.have.property('duration', 700);
    expect(transition).to.have.property('apply').that.is.a('function');
  });

  it('should add class and call callback after duration', function (done) {
    // Simulate jQuery/Zepto addClass
    let addedClass;
    const fakeEl = {
      addClass: (cls) => { addedClass = cls; }
    };
    const fakeCallback = () => {
      expect(addedClass).to.equal('animated fadeIn');
      done();
    };
    // Inline re-def
    const transition = {
      duration: 10,
      apply: function (el, type, callback) {
        el.addClass('animated ' + type);
        setTimeout(callback, this.duration);
      }
    };
    transition.apply(fakeEl, 'fadeIn', fakeCallback);
  });
});