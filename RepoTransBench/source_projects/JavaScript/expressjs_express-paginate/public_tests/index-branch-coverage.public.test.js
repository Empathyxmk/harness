const paginate = require('../index');
const expect = require('chai').expect;
const reqres = require('reqres');

describe('express-paginate - additional branch and error coverage (public data)', function () {
  describe('.href', function () {
    it('should clamp page to 1 if prev=true from page 2', function () {
      const req = { originalUrl: '/bar', query: { page: '2' } };
      // page will be parsed to 2, then prev reduces to 1 -> clamped to 1 if reduced again
      const href = paginate.href(req);
      const out = href(true);
      expect(out).to.match(/page=1/);
    });
    it('should add params even when not object', function () {
      const req = { originalUrl: '/bar', query: { page: '5' } };
      const href = paginate.href(req);
      expect(href(false, undefined)).to.match(/page=6/);
      expect(href(false, null)).to.match(/page=6/);
    });
  });

  describe('.hasNextPages', function () {
    it('should throw if pageCount < 0', function () {
      const req = { query: { page: 2 } };
      expect(() => paginate.hasNextPages(req)(-3)).to.throw(/not a number >= 0/);
    });
    it('should throw if pageCount not a number', function () {
      const req = { query: { page: 2 } };
      expect(() => paginate.hasNextPages(req)("abc")).to.throw(/not a number/);
    });
    it('should handle 0 pages', function () {
      const req = { query: { page: 2 } };
      expect(paginate.hasNextPages(req)(0)).to.equal(false);
    });
  });

  describe('.getArrayPages', function () {
    const mkreq = () => ({ originalUrl: '/baz', query: { page: 7 } });

    it('should throw if currentPage is not a number', function () {
      expect(() => paginate.getArrayPages(mkreq())(4, 20, 'foo')).to.throw(/currentPage/);
      expect(() => paginate.getArrayPages(mkreq())(4, 20, -5)).to.throw(/currentPage/);
    });

    it('should throw if pageCount is < 0 or not a number', function () {
      expect(() => paginate.getArrayPages(mkreq())(2, -2, 1)).to.throw(/pageCount/);
      expect(() => paginate.getArrayPages(mkreq())(2, "bar", 1)).to.throw(/pageCount/);
    });

    it('should throw if limit is < 0 or not a number', function () {
      expect(() => paginate.getArrayPages(mkreq())(-5, 5, 1)).to.throw(/limit/);
      expect(() => paginate.getArrayPages(mkreq())("baz", 5, 1)).to.throw(/limit/);
    });

    it('should default limit to 3 and give correct range', function () {
      const req = mkreq();
      const arr = paginate.getArrayPages(req)(undefined, 30, 7);
      expect(arr).to.be.an('array');
      expect(arr.length).to.be.eql(3);
      expect(arr[0].number).to.equal(6);
    });

    it('should return full array if limit is 0 (library returns all, not empty array)', function () {
      const req = mkreq();
      // This test expects the current implementation: limit 0 returns as if limit 3.
      const arr = paginate.getArrayPages(req)(0, 15, 5);
      expect(arr).to.be.an('array');
      expect(arr.length).to.be.greaterThan(0);
    });
  });

  describe('.middleware', function () {
    it('should default params if not provided', function (done) {
      const req = reqres.req({ query: {} });
      const res = reqres.res();
      paginate.middleware(undefined, undefined)(req, res, () => {
        expect(req.query.page).to.equal(1);
        expect(req.query.limit).to.equal(10);
        expect(res.locals.paginate.hasPreviousPages).to.be.false;
        expect(typeof res.locals.paginate.href).to.equal('function');
        expect(typeof res.locals.paginate.hasNextPages).to.equal('function');
        expect(typeof res.locals.paginate.getArrayPages).to.equal('function');
        done();
      });
    });
    it('should clamp limit to maxLimit', function (done) {
      const req = reqres.req({ query: { limit: '100', page: '3' } });
      const res = reqres.res();
      paginate.middleware(7, 9)(req, res, () => {
        expect(req.query.limit).to.equal(9);
        done();
      });
    });
    it('should clamp negative limit', function (done) {
      const req = reqres.req({ query: { limit: '-10' } });
      const res = reqres.res();
      paginate.middleware()(req, res, () => {
        expect(req.query.limit).to.equal(0);
        done();
      });
    });
    it('should clamp negative page', function (done) {
      const req = reqres.req({ query: { page: '-12' } });
      const res = reqres.res();
      paginate.middleware()(req, res, () => {
        expect(req.query.page).to.equal(1);
        done();
      });
    });
    it('should deal with non-string page/limit', function (done) {
      const req = reqres.req({ query: { page: 5, limit: 12 } });
      const res = reqres.res();
      paginate.middleware()(req, res, () => {
        expect(req.query.page).to.equal(1);
        expect(req.query.limit).to.equal(10);
        done();
      });
    });
    it('should compute skip and offset properly', function (done) {
      const req = reqres.req({ query: { page: '4', limit: '7' } });
      const res = reqres.res();
      paginate.middleware()(req, res, () => {
        expect(req.skip).to.equal(21);
        expect(req.offset).to.equal(21);
        done();
      });
    });
  });
});