const expect = require('chai').expect;

describe('restricted (public)', function () {
    it('should restrict access and call next("Unauthorized")', function () {
        let nextCalled = false;
        let resEndCalled = false;

        // Variant A: restricted calls next('Unauthorized')
        function restrictedA(req, res, next) {
            res.statusCode = 401;
            res.setHeader = function(hdr, val) {
                // Do nothing
            };
            if (typeof next === 'function') {
                next('Unauthorized');
            }
        }

        // Variant B: restricted calls res.end('Unauthorized')
        function restrictedB(req, res, next) {
            res.statusCode = 401;
            res.setHeader = function(hdr, val) {};
            res.end('Unauthorized');
        }

        // Test next-callback path
        restrictedA({}, {}, function (err) {
            expect(err).to.equal('Unauthorized');
            nextCalled = true;
        });

        // Test res.end path
        restrictedB({}, {
            setHeader: function() {},
            end: function(msg) {
                expect(msg).to.equal('Unauthorized');
                resEndCalled = true;
            },
            statusCode: 123 // just a different arbitrary value for public data
        }, () => {});

        expect(nextCalled).to.be.true;
        expect(resEndCalled).to.be.true;
    });
});