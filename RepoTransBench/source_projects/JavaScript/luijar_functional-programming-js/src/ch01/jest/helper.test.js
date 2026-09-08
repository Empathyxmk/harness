const helper = require('../helper.js');
const Person = require('../../model/Person.js').Person;

describe('ch01/helper.js', () => {
  it('should export db with find method', () => {
    expect(helper.db).toBeDefined();
    expect(typeof helper.db.find).toBe('function');
  });

  it('should return Person if ssn exists as key', () => {
    const person = helper.db.find('444-44-4444');
    expect(person).toBeInstanceOf(Person);
    expect(person.ssn).toBe('444-44-4444');
    expect(person.firstname).toBe('Alonzo');
    expect(person.lastname).toBe('Church');
  });

  it('should support alternate ssn lookup', () => {
    // This will match '444444444' key but Person created with '444-44-4444'
    const person = helper.db.find('444444444');
    expect(person).toBeInstanceOf(Person);
    expect(person.ssn).toBe('444-44-4444');
  });

  it('should return undefined for unknown ssn', () => {
    const person = helper.db.find('not-a-ssn');
    expect(person).toBeUndefined();
  });
});