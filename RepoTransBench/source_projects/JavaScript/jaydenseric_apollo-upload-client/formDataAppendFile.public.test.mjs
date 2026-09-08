import { formDataAppendFile } from './formDataAppendFile.mjs';

function runTest() {
  // Public scenario: use different values!
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
  const field = 'avatar';
  const file = { type: 'image/png', content: 'PNGDATA' };
  const fileName = 'avatar-2024.png';

  formDataAppendFile(fakeFormData, field, file, fileName);
  if (
    appendedField !== field ||
    appendedFile !== file ||
    appendedFileName !== fileName
  ) {
    throw new Error('Appended values do not match expected values');
  }
  console.log('formDataAppendFile.public.test.mjs passed');
}
runTest();