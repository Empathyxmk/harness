import { createUploadLink } from './createUploadLink.mjs';

function runTest() {
  // Use different input data:
  const options = { uri: '/files', credentials: 'same-origin', headers: { 'x-test-header': 'abc123' } };
  const link = createUploadLink(options);

  if (!link || typeof link !== 'object' || link.isUploadLink !== true) {
    throw new Error('Should return an object indicating isUploadLink: true');
  }
  // Must match the new test data
  if (JSON.stringify(link.options) !== JSON.stringify(options)) {
    throw new Error('Returned options property does not match test options');
  }

  console.log('createUploadLink.public.test.mjs passed');
}

runTest();