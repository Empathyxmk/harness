const createNode = require('../src/nodeCreator');

describe('nodeCreator extra branch coverage - public', function(){
    it('should return value for null, undefined, boolean (public)', function(){
        expect(createNode(null)).toBe(null);
        expect(createNode(undefined)).toBe(undefined);
        expect(createNode(true)).toBe(true);
    });
    it('should create frozen array/object with deep data (public)', function(){
        let obj = createNode({ arr: [{ deep: 5 }] });
        expect(Object.isFrozen(obj)).toBe(true);
        expect(Object.isFrozen(obj.arr)).toBe(true);
        expect(Object.isFrozen(obj.arr[0])).toBe(true);
        expect(obj.arr[0].deep).toBe(5);
    });
});