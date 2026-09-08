const test = require('tape')

// Basic add function test
test('add: adds numbers correctly', t => {
  function add(a, b) {
    return a + b
  }
  t.equal(add(1, 2), 3)
  t.equal(add(-1, 1), 0)
  t.equal(add(0, 0), 0)
  t.end()
})

// Check if string is palindrome
test('isPalindrome: detects palindromes', t => {
  function isPalindrome(str) {
    return str === str.split('').reverse().join('')
  }
  t.equal(isPalindrome('racecar'), true)
  t.equal(isPalindrome('hello'), false)
  t.equal(isPalindrome('madam'), true)
  t.end()
})