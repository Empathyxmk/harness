/* eslint-disable */
/* global describe, it */

const should = require('should');
const fs = require('fs');
const path = require('path');
const gulp = require('gulp');
const Vinyl = require('vinyl');
const es = require('event-stream');
const inlineCss = require('../index');

/**
 * Utility to get a Vinyl file from fixture path.
 */
function getFile(filePath) {
    return new Vinyl({
        path: path.resolve(filePath),
        cwd: './public_tests/',
        base: path.dirname(filePath),
        contents: Buffer.from(String(fs.readFileSync(filePath)))
    });
}

/**
 * Compare the output of inlining with an expected result file.
 */
function compare(fixturePath, expectedPath, options, done) {
    const stream = inlineCss(options);

    stream.write(getFile(fixturePath));

    stream.once('data', file => {
        should.ok(file.isBuffer());
        file.contents.toString('utf8').should.be.equal(String(fs.readFileSync(expectedPath)));
        done();
    });
}

describe('gulp-inline-css PUBLIC TESTS', () => {
    it('file should pass through using different content', done => {
        let a = 0;

        const fakeFile = new Vinyl({
            path: '/public_tests/fixture/testfile.html',
            cwd: '/public_tests/',
            base: '/public_tests/fixture/',
            contents: Buffer.from('Public Test Case!')
        });

        const stream = inlineCss();

        stream.on('data', newFile => {
            should.ok(newFile.contents);
            should.equal(newFile.path, path.normalize('/public_tests/fixture/testfile.html'));
            should.equal(newFile.relative, 'testfile.html');
            ++a;
        });

        stream.once('end', () => {
            should.equal(a, 1);
            done();
        });

        stream.write(fakeFile);
        stream.end();
    });

    it('should let null files pass through (public)', done => {
        const stream = inlineCss();
        let n = 0;

        stream.pipe(es.through(file => {
            should.equal(file.path, 'public-null.md');
            should.equal(file.contents,  null);
            n++;
        }, () => {
            should.equal(n, 1);
            done();
        }));

        stream.write(new Vinyl({
            path: 'public-null.md',
            contents: null
         }));

        stream.end();
    });

    it('should emit error on streamed file (public)', done => {
      gulp.src(path.join('public_tests', 'fixtures', 'inline.html'), { buffer: false })
        .pipe(inlineCss())
        .on('error', ({message}) => {
          message.should.equal('Streaming not supported');
          done();
        });
    });

    it('Should convert linked css to inline css (public/alt data)', done => {
        const options = {};
        compare(
          path.join('public_tests', 'fixtures', 'inline.html'),
          path.join('public_tests', 'expected', 'inline-expected.html'),
          options,
          done
        );
    });

    it('Should inline css in multiple HTML files (public/alt data)', done => {
        const options = {};
        compare(
            path.join('public_tests', 'fixtures', 'group', 'alpha', 'inline.html'),
            path.join('public_tests', 'expected', 'group', 'alpha', 'inline-expected.html'),
            options,
            () => {}
        );
        compare(
            path.join('public_tests', 'fixtures', 'group', 'beta', 'inline.html'),
            path.join('public_tests', 'expected', 'group', 'beta', 'inline-expected.html'),
            options,
            done
        );
    });

    it('Should ignore hbs code blocks (public)', done => {
        const options = {};
        compare(
            path.join('public_tests', 'fixtures', 'codeblocks-public.html'),
            path.join('public_tests', 'expected', 'codeblocks-public.html'),
            options,
            done
        );
    });

    it('Should ignore user defined code blocks (public)', done => {
        const options = {
            codeBlocks: {
                special: { start: '<!', end: '!>' }
            }
        };
        compare(
            path.join('public_tests', 'fixtures', 'codeblocks-external-public.html'),
            path.join('public_tests', 'expected', 'codeblocks-external-public.html'),
            options,
            done
        );
    });
});