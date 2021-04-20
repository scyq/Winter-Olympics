/**
 * Convert a file to local URL
 *
 * @param {File} file
 * @returns {string} a fetchable url
 */
export function file2URL(file) {
    return URL.createObjectURL(file);
}