const Freezer = require('../src/freezer');

describe('Freezer coverage - public cases', function() {
    it('should initialize with an object and get correct toJS', function() {
        var f = new Freezer({z: 5, w: [7, 8]});
        var obj = f.get();
        expect(obj.z).toBe(5);
        expect(obj.w[1]).toBe(8);
        expect(obj.toJS()).toEqual({z: 5, w: [7, 8]});
    });

    it('should set and update data correctly', function() {
        var f = new Freezer({p: 1});
        var obj = f.get();
        obj.set({q: 2});
        expect(obj.q).toBe(2);
        expect(obj.p).toBe(undefined);
    });

    it('should add nodes and push correctly (public data)', function() {
        var f = new Freezer([{val: 100}]);
        var arr = f.get();
        arr.push({val: 200});
        expect(arr.length).toBe(2);
        expect(arr[1].val).toBe(200);
    });

    it('should reset and replace data (public)', function() {
        var f = new Freezer({original: 10});
        var obj = f.get();
        f.set({replaced: "yes"});
        var obj2 = f.get();
        expect(obj2.original).toBe(undefined);
        expect(obj2.replaced).toBe("yes");
    });

    it('should emit update events (public)', function(done) {
        var f = new Freezer({change: 25});
        var updated = false;
        f.get().on('update', function() {
            updated = true;
            expect(updated).toBe(true);
            done();
        });
        f.get().set({change: 26});
    });
});