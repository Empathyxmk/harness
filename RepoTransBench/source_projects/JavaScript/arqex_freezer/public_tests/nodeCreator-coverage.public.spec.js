const createNode = require('../src/nodeCreator');

describe('nodeCreator public coverage', function(){
    it('should create a frozen array (public)', function(){
        let arr = createNode([100, 200]);
        expect(Array.isArray(arr)).toBe(true);
        expect(arr[0]).toBe(100);
        expect(Object.isFrozen(arr)).toBe(true);
    });

    it('should create a frozen object (public)', function(){
        let obj = createNode({foo: 7, bar: 8});
        expect(typeof obj).toBe('object');
        expect(obj.foo).toBe(7);
        expect(Object.isFrozen(obj)).toBe(true);
    });

    it('should return primitives as is (public)', function(){
        expect(createNode("sample")).toBe("sample");
        expect(createNode(555)).toBe(555);
        expect(createNode(false)).toBe(false);
    });
});