// Slightly refactor to ensure exports for testability

const fs = require('fs')
const path = require('path')
const jsonlint = require('jsonlint')
const utils = require('./utils')

function checkGeoJSON() {
  let passed = true
  utils.cities.forEach(city => {
    const file = utils.getCityGeoJSON(city)
    if (!fs.existsSync(file)) {
      console.warn(`Not found: ${file}`)
      passed = false
      return
    }
    try {
      const raw = fs.readFileSync(file, 'utf8')
      const geo = jsonlint.parse(raw)
      if (!geo.features || !Array.isArray(geo.features)) {
        console.error(`Bad geojson structure in ${file}`)
        passed = false
        return
      }
      geo.features.forEach((f, i) => {
        if (!f.properties)
          console.warn(`Feature ${i} missing properties: ${city}`)
      })
    } catch (e) {
      console.error(`Parse error in ${file}: ${e.message}`)
      passed = false
    }
  })
  if (passed) console.log('GeoJSON check pass.')
}

function getCafeNumberFromGeo(city) {
  const file = utils.getCityGeoJSON(city)
  if (!fs.existsSync(file)) return 0
  const raw = fs.readFileSync(file, 'utf8')
  const geo = jsonlint.parse(raw)
  return geo.features ? geo.features.length : 0
}

function getCafeNumbersFromReadme() {
  const readme = fs.readFileSync(path.resolve(__dirname, '../README.md'), 'utf-8')
  const ptn = /\|\s*([^\|\n]+?)\s*\|\s*(\d+)\s*\|/g
  const obj = {}
  let m
  while ((m = ptn.exec(readme))) {
    obj[m[1].trim()] = Number(m[2])
  }
  return obj
}

function isCounterMatched(city, realNum) {
  const rd = getCafeNumbersFromReadme()
  return rd[city] === realNum
}

function checkNumbers() {
  let passed = true
  utils.cities.forEach(city => {
    const realNum = getCafeNumberFromGeo(city)
    if (!isCounterMatched(city, realNum)) {
      console.log(`Found inconsistent number: city = ${city}, newNum = ${realNum}`)
      passed = false
    }
  })
  if (passed) console.log('Cafe number check pass.')
}

function updateCafeNumbers() {
  const file = path.resolve(__dirname, '../README.md')
  let text = fs.readFileSync(file, 'utf-8')
  utils.cities.forEach(city => {
    const num = getCafeNumberFromGeo(city)
    // Update: make sure we match the correct city line
    const cityRegex = new RegExp(`(\\|\\s*${city}\\s*\\|\\s*)\\d+(\\s*\\|)`)
    text = text.replace(cityRegex, `$1${num}$2`)
  })
  fs.writeFileSync(file, text)
  console.log('Updating README.md, don’t forget to commit it!')
}

module.exports = {
  checkGeoJSON,
  checkNumbers,
  updateCafeNumbers,
  getCafeNumbersFromReadme,
  getCafeNumberFromGeo,
  isCounterMatched,
}