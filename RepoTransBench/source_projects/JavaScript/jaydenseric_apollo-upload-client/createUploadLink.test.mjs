import { createUploadLink } from './createUploadLink.mjs';

function runTest() {
  // Classic test data:
  const options = { uri: '/graphql', credentials: 'include', headers: { 'x-test': 'foo' } };
  const link = createUploadLink(options);
  if (!link || typeof link !== 'object' || link.isUploadLink !== true) {
    throw new Error('Should return an object indicating isUploadLink: true');
  }
  if (JSON.stringify(link.options) !== JSON.stringify(options)) {
    throw new Error('Returned options property does not match');
  }

  console.log('createUploadLink.test.mjs passed');
}

runTest();