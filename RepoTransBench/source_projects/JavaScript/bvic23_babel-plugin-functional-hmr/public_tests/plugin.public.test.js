const plugin = require('../index.js');
const fs = require('fs');
const path = require('path');
const core = require('babel-core');

const f = file => path.join(__dirname, '..', '__fixtures_public__', file);
const read = file => fs.readFileSync(f(file), 'utf8');
const given = file => ({ source: read(`${file}.public.js`) });
const l = string => string.trim().split('\n').filter(l => l !== '/* eslint-disable */');
const transform = source => core.transform(source, { plugins: [plugin], filename: '%%FILENAME%%' }).code;

test('already a class, should not transform anything (public case)', () => {
    // Given
    const { source } = given('class-already');

    // When
    const code = transform(source);

    // Then
    expect(l(code)).toMatchSnapshot();
});

test('function, should transform (public case)', () => {
    // Given
    const { source } = given('export-default-param');

    // When
    const code = transform(source);

    // Then
    expect(l(code)).toMatchSnapshot();
});

test('function as const, should transform (public case)', () => {
    // Given
    const { source } = given('declared-as-const');

    // When
    const code = transform(source);

    // Then
    expect(l(code)).toMatchSnapshot();
});

test('simple function, should not change (public case)', () => {
    // Given
    const { source } = given('simplefunction');

    // When
    const code = transform(source);

    // Then
    expect(l(code)).toMatchSnapshot();
});

test('multiple components, should change (public case)', () => {
    // Given
    const { source } = given('multiple-components');

    // When
    const code = transform(source);

    // Then
    expect(l(code)).toMatchSnapshot();
});

test('embedded return, should change (public case)', () => {
    // Given
    const { source } = given('embedded-return');

    // When
    const code = transform(source);

    // Then
    expect(l(code)).toMatchSnapshot();
});