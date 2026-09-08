import { formDataAppendFile } from './formDataAppendFile.mjs';

function runTest() {
  // Existing (classic) test scenario
  let appendedField = '';
  let appendedFile = null;
  let appendedFileName = '';
  const fakeFormData = {
    append: (f, fl, fn) => {
      appendedField = f;
      appendedFile = fl;
      appendedFileName = fn;
    }
  };
  const field = 'fileUpload';
  const file = { type: 'text/plain', content: 'Sample test' };
  const fileName = 'test.txt';

  formDataAppendFile(fakeFormData, field, file, fileName);
  if (
    appendedField !== field ||
    appendedFile !== file ||
    appendedFileName !== fileName
  ) {
    throw new Error('Appended values do not match expected inputs');
  }
  console.log('formDataAppendFile.test.mjs passed');
}
runTest();