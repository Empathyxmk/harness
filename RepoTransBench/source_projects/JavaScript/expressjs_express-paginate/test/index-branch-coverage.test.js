const paginate = require('../index');
const expect = require('chai').expect;
const reqres = require('reqres');

describe('express-paginate - additional branch and error coverage', function () {
  describe('.href', function () {
    it('should clamp page to 1 if prev=true from page 1', function () {
      const req = { originalUrl: '/foo', query: { page: '1' } };
      // page will be parsed to 1, then prev reduces to 0 -> clamped to 1
      const href = paginate.href(req);
      const out = href(true);
      expect(out).to.match(/page=1/);
    });
    it('should add params even when not object', function () {
      const req = { originalUrl: '/foo', query: { page: '3' } };
      const href = paginate.href(req);
      // params as undefined, which is not object
      expect(href(false, undefined)).to.match(/page=4/);
      // params as null, which is not object
      expect(href(false, null)).to.match(/page=4/);
    });
  });

  describe('.hasNextPages', function () {
    it('should throw if pageCount < 0', function () {
      const req = { query: { page: 1 } };
      expect(() => paginate.hasNextPages(req)(-1)).to.throw(/not a number >= 0/);
    });
    it('should throw if pageCount not a number', function () {
      const req = { query: { page: 1 } };
      expect(() => paginate.hasNextPages(req)("foo")).to.throw(/not a number/);
    });
    it('should handle 0 pages', function () {
      const req = { query: { page: 1 } };
      expect(paginate.hasNextPages(req)(0)).to.equal(false);
    });
  });

  describe('.getArrayPages', function () {
    const mkreq = () => ({ originalUrl: '/bar', query: { page: 4 } });

    it('should throw if currentPage is not a number', function () {
      expect(() => paginate.getArrayPages(mkreq())(3, 10, 'bar')).to.throw(/currentPage/);
      expect(() => paginate.getArrayPages(mkreq())(3, 10, -2)).to.throw(/currentPage/);
    });

    it('should throw if pageCount is < 0 or not a number', function () {
      expect(() => paginate.getArrayPages(mkreq())(3, -1, 1)).to.throw(/pageCount/);
      expect(() => paginate.getArrayPages(mkreq())(3, "foo", 1)).to.throw(/pageCount/);
    });

    it('should throw if limit is < 0 or not a number', function () {
      expect(() => paginate.getArrayPages(mkreq())(-1, 5, 1)).to.throw(/limit/);
      expect(() => paginate.getArrayPages(mkreq())("foo", 5, 1)).to.throw(/limit/);
    });

    it('should default limit to 3 and give correct range', function () {
      const req = mkreq();
      const arr = paginate.getArrayPages(req)(undefined, 10, 4);
      expect(arr).to.be.an('array');
      expect(arr.length).to.be.eql(3);
      expect(arr[0].number).to.equal(3);
    });

    it('should return full array if limit is 0 (library returns all, not empty array)', function () {
      const req = mkreq();
      // This test expects the current implementation: limit 0 returns as if limit 3.
      const arr = paginate.getArrayPages(req)(0, 10, 3);
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
      const req = reqres.req({ query: { limit: '900', page: '2' } });
      const res = reqres.res();
      paginate.middleware(5, 8)(req, res, () => {
        expect(req.query.limit).to.equal(8);
        done();
      });
    });
    it('should clamp negative limit', function (done) {
      const req = reqres.req({ query: { limit: '-3' } });
      const res = reqres.res();
      paginate.middleware()(req, res, () => {
        expect(req.query.limit).to.equal(0);
        done();
      });
    });
    it('should clamp negative page', function (done) {
      const req = reqres.req({ query: { page: '-32' } });
      const res = reqres.res();
      paginate.middleware()(req, res, () => {
        expect(req.query.page).to.equal(1);
        done();
      });
    });
    it('should deal with non-string page/limit', function (done) {
      const req = reqres.req({ query: { page: 3, limit: 5 } });
      const res = reqres.res();
      paginate.middleware()(req, res, () => {
        expect(req.query.page).to.equal(1);
        expect(req.query.limit).to.equal(10);
        done();
      });
    });
    it('should compute skip and offset properly', function (done) {
      const req = reqres.req({ query: { page: '2', limit: '10' } });
      const res = reqres.res();
      paginate.middleware()(req, res, () => {
        expect(req.skip).to.equal(10);
        expect(req.offset).to.equal(10);
        done();
      });
    });
  });
});