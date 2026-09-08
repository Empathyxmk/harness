import { isExtractableFile } from './isExtractableFile.mjs';

function runTest() {
  // Public test - different data, same logic coverage
  if (isExtractableFile('a string') !== false) throw new Error('string not extractable');
  if (isExtractableFile([]) !== false) throw new Error('array not extractable');
  if (isExtractableFile({}) !== false) throw new Error('empty object not extractable');
  if (isExtractableFile({ name: 'blob' }) !== false) throw new Error('object without type not extractable');
  if (isExtractableFile({ type: 'application/pdf' }) !== true) throw new Error('object with pdf type should be extractable');
  if (isExtractableFile({ type: 'custom-type', extra: true }) !== true) throw new Error('object with type and extra fields extractable');
  console.log('isExtractableFile.public.test.mjs passed');
}
runTest();