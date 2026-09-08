// datehisto.js - minimally export a function/object to allow coverage

module.exports = {
  formatDate: function (d) {
    if (!d) return '';
    const date = new Date(d);
    if (isNaN(date.getTime())) return 'Invalid';
    return date.toISOString().split('T')[0];
  }
};