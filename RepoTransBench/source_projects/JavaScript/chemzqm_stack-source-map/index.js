// PATCH: Guard 'location' access to allow execution in Node and browser!
module.exports = function (option) {
  option = option || {}
  // patch: guard access with typeof location !== 'undefined'
  if (typeof location !== 'undefined' && /^file/i.test(location.protocol)) {
    console.warn('stack-source-map not works on file protocol')
  } else {
    var prepareStackTrace = option.prepareStackTrace || function (err, structuredStackTrace) {
      return structuredStackTrace
        .map(function (callSite) {
          var fn = callSite.getFunctionName() || '<anonymous>'
          var file = callSite.getFileName()
          var line = callSite.getLineNumber()
          var col = callSite.getColumnNumber()
          return fn + ' (' + file + ':' + line + ':' + col + ')'
        })
        .join('\n')
    }
    Error.prepareStackTrace = prepareStackTrace
  }
}