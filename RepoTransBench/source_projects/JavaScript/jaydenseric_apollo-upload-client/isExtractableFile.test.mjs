import { isExtractableFile } from './isExtractableFile.mjs';

function runTest() {
  // Existing test: Basic checks on extractability logic.
  if (isExtractableFile(undefined) !== false) throw new Error('undefined not extractable');
  if (isExtractableFile(null) !== false) throw new Error('null not extractable');
  if (isExtractableFile(123) !== false) throw new Error('number not extractable');
  if (isExtractableFile({ foo: 'bar' }) !== false) throw new Error('object without type not extractable');
  if (isExtractableFile({ type: 'image/gif' }) !== true) throw new Error('object with type should be extractable');
  if (isExtractableFile({ type: '', foo: 'bar' }) !== true) throw new Error('object with type property should be extractable');
  console.log('isExtractableFile.test.mjs passed');
}
runTest();