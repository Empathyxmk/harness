const Queue = require('../../lib/dataStructures/queue');

const publicValue1 = 'alpha_value1';
const publicValue2 = 'beta_value2';

describe('When adding two new elements to a Queue (public test)', () => {
  let myQueue;

  beforeEach(() => {
    myQueue = new Queue();
    myQueue
      .push(publicValue1)
      .push(publicValue2);
  });

  it('the Queue`s length should be 2', () => {
    expect(myQueue.length).toBe(2);
  });

  describe('then removing an element', () => {
    let result;

    beforeEach(() => {
      result = myQueue.pop();
    });

    it('the Queue`s length should be 1', () => {
      expect(myQueue.length).toBe(1);
    });

    it('the element removed should be the first element added.', () => {
      expect(result).toBe(publicValue1);
    });
  });

  describe('then removing 2 elements', () => {
    let result1, result2;

    beforeEach(() => {
      result1 = myQueue.pop();
      result2 = myQueue.pop();
    });

    it('the Queue`s length should be 0', () => {
      expect(myQueue.length).toBe(0);
    });

    it('the elements removed should be in the order to which they were added.', () => {
      expect(result1).toBe(publicValue1);
      expect(result2).toBe(publicValue2);
    });
  });
});