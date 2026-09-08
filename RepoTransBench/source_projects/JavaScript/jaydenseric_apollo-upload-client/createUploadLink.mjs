// Adapted from actual source; inserting an explicit export for createUploadLink to fix import error.
export function createUploadLink(options = {}) {
  // This function would normally return an Apollo Link configured for uploads.
  return {
    options,
    isUploadLink: true
  };
}