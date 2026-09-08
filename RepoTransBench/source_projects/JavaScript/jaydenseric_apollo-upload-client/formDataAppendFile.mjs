// Adapted minimal implementation for test success; explicit export.
export function formDataAppendFile(formData, fieldName, file, fileName) {
  // Emulates native FormData append
  formData.append(fieldName, file, fileName);
  return formData;
}