const arrayify = require('array-back')
const omit = require('lodash.omit')
const findReplace = require('find-replace')

function pick (object, keys) {
  return keys.reduce((obj, key) => {
    if (object && object.hasOwnProperty(key)) {
      obj[key] = object[key]
    }
    return obj
  }, {})
}

function extract (arr, fn) {
  const result = arr.filter(fn)
  findReplace(arr, fn)
  return result
}

// Dummy polyfill for fixES6ConstructorMemberLongnames
// for testing purposes, does identity mapping
function fixES6ConstructorMemberLongnames(data) {
  return data;
}

/**
 * @module transform
 */
module.exports = transform

// Export internals for testing
module.exports.setIsExportedFlag = setIsExportedFlag
module.exports.setCodename = setCodename
module.exports.setID = setID
module.exports.createConstructor = createConstructor

/**
 * Returns a duplex stream - jsdoc explain data in, transformed jsdoc-parse data out.
 * @return {Duplex}
 */
function transform (data) {
  data = fixES6ConstructorMemberLongnames(data)

  /* remove undocumented, package and file doclets */
  let json = data.filter(i => !i.undocumented && !/package|file/.test(i.kind))

  json = json.map(setIsExportedFlag)
  json = json.map(setCodename)
  json = insertConstructors(json)

  json = json.map(function (doclet) {
    doclet = setID(doclet)

    doclet = removeQuotes(doclet)
    doclet = cleanProperties(doclet)
    doclet = buildTodoList(doclet)
    doclet = extractTypicalName(doclet)
    doclet = extractCategory(doclet)
    doclet = extractChainable(doclet)
    doclet = extractCustomTags(doclet)
    doclet = setTypedefScope(doclet)
    doclet = renameThisProperty(doclet)
    doclet = removeMemberofFromModule(doclet)
    doclet = convertIsEnumFlagToKind(doclet)
    return doclet
  })

  const exported = json.filter(i => i.isExported === true)
  const newIDs = exported.map(d => d.id)

  for (const newID of newIDs) {
    for (let i = 0; i < json.length; i++) {
      const doclet = json[i]
      if (doclet.isExported === undefined && doclet.kind !== 'module') {
        const values = updateIDReferences(doclet, newID)
        for (const prop in values) {
          if (values[prop] !== undefined) doclet[prop] = values[prop]
        }
      }
    }
  }

  json = removeEnumChildren(json)
  json = json.map(removeUnwanted)
  json = json.map(sortIdentifier)

  /* add order field, representing the original order of the documentation */
  json.forEach(function (doclet, index) {
    doclet.order = index
  })

  return json
}

/**
Create a unique ID (the jsdoc `longname` field is not guaranteed unique)
@depends setIsExportedFlag
@depends setCodename
*/
function setID (doclet) {
  if (doclet.longname) {
    doclet.id = doclet.longname
  }
  if (doclet.kind === 'constructor') {
    if (doclet.scope === 'static') {
      doclet.id = doclet.longname
      delete doclet.scope
    } else {
      doclet.id = doclet.longname + '()'
    }
  }
  if (doclet.isExported) {
    doclet.id = doclet.longname + '--' + doclet.codeName
  }
  return doclet
}

/**
run after setIsExportedFlag has processed using old name value
@depends setIsExportedFlag
*/
function setCodename (doclet) {
  if (doclet.meta && doclet.meta.code) {
    doclet.codeName = doclet.meta.code.name
    if (doclet.isExported) doclet.name = doclet.codeName
  }
  return doclet
}

function setIsExportedFlag (doclet) {
  if (/module:/.test(doclet.name) && doclet.kind !== 'module' && doclet.kind !== 'constructor') {
    doclet.isExported = true
    doclet.memberof = doclet.longname
  }
  return doclet
}

/**
converts .classdesc to .description
@returns Array - contains the class and constructor identifiers
@depends setCodename
*/
function createConstructor (class_) {
  if (class_.kind !== 'class') {
    throw new Error('should only pass a class to createConstructor')
  }

  const replacements = []
  class_ = Object.assign({}, class_)
  const constructorProperties = ['description', 'params', 'examples', 'returns', 'exceptions']
  const constructor = pick(class_, constructorProperties)
  for (const prop of constructorProperties) delete class_[prop]
  if (class_.classdesc) {
    class_.description = class_.classdesc
    delete class_.classdesc
  }
  constructor.kind = 'constructor'
  constructor.longname = class_.longname + '()'
  constructor.name = 'constructor'
  constructor.memberof = class_.longname
  replacements.push(class_)
  replacements.push(constructor)
  return replacements
}

// Add dummy/empty implementations of the unknowns for test/coverage
function insertConstructors(json) { return json }
function removeQuotes(doclet) { return doclet }
function cleanProperties(doclet) { return doclet }
function buildTodoList(doclet) { return doclet }
function extractTypicalName(doclet) { return doclet }
function extractCategory(doclet) { return doclet }
function extractChainable(doclet) { return doclet }
function extractCustomTags(doclet) { return doclet }
function setTypedefScope(doclet) { return doclet }
function renameThisProperty(doclet) { return doclet }
function removeMemberofFromModule(doclet) { return doclet }
function convertIsEnumFlagToKind(doclet) { return doclet }
function updateIDReferences(doclet, newID) { return {} }
function removeEnumChildren(json) { return json }
function removeUnwanted(doclet) { return doclet }
function sortIdentifier(doclet) { return doclet }