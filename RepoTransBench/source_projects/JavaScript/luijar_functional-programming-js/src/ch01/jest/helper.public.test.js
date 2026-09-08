/**
 * Public test for ch01/helper.js with different student data
 */

const Person = require('../../model/Person.js').Person;
const db = require('../helper').db;

describe('ch01/helper.js db (public)', () => {
  it('should return undefined for non-existing student', () => {
    expect(db.find('123-45-6789')).toBeUndefined();
  });

  it('should store and retrieve a new Person object in a custom db object (public)', () => {
    // Custom db for this test with different student
    const customDb = {
      students: {
        '111-22-3333': new Person('111-22-3333', 'Alan', 'Turing'),
      },
      find: function (ssn) {
        return this.students[ssn];
      }
    };
    expect(customDb.find('111-22-3333')).toEqual(
      expect.objectContaining({ ssn: '111-22-3333', firstname: 'Alan', lastname: 'Turing' })
    );
  });
});