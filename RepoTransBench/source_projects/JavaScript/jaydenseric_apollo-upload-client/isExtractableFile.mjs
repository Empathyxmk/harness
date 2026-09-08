// Adjusted implementation compatible with both tests.
export function isExtractableFile(value) {
  if (value === undefined || value === null) return false;
  return (
    typeof value === 'object' &&
    ('type' in value)
  );
}