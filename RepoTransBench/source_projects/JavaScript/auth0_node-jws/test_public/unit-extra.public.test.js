const test = require('tape')

// Basic add function test with different numbers
test('add: adds numbers (public test data)', t => {
  function add(a, b) {
    return a + b
  }
  t.equal(add(10, 7), 17)
  t.equal(add(-3, 3), 0)
  t.equal(add(42, 0), 42)
  t.end()
})

// Check if string is palindrome with different data
test('isPalindrome: public palindrome cases', t => {
  function isPalindrome(str) {
    return str === str.split('').reverse().join('')
  }
  t.equal(isPalindrome('noon'), true)
  t.equal(isPalindrome('world'), false)
  t.equal(isPalindrome('rotator'), true)
  t.end()
})