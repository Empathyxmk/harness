const { Developer, Tester } = require('../Template');

describe('Template Pattern Employee', () => {
  test('Developer responsibilities and pay', () => {
    const dev = new Developer('Alice', 1500);
    expect(dev.work()).toBe('Alice handles application development');
    expect(dev.getPaid()).toBe('Alice got paid 1500');
  });

  test('Tester responsibilities and pay', () => {
    const qa = new Tester('Bob', 900);
    expect(qa.work()).toBe('Bob handles testing');
    expect(qa.getPaid()).toBe('Bob got paid 900');
  });

  test('Developer responsibilities method override', () => {
    class CustomDev extends Developer {
      responsibilities() {
        return 'custom stuff';
      }
    }
    const cDev = new CustomDev('Eve', 1200);
    expect(cDev.work()).toBe('Eve handles custom stuff');
  });
});