// Example IP Camera utility functions for demonstration

function getSnapshotUrl(baseUrl, cameraId) {
    if (!baseUrl || !cameraId) {
        throw new Error('Missing arguments');
    }
    if (!/^https?:\/\//.test(baseUrl)) {
        throw new Error('Invalid baseUrl');
    }
    return `${baseUrl}/camera/${cameraId}/snapshot`;
}

function isOnline(statusObj) {
    // statusObj example: { connected: true, lastPing: 1234 }
    if (!statusObj || typeof statusObj.connected !== 'boolean') {
        return false;
    }
    return statusObj.connected;
}

module.exports = { getSnapshotUrl, isOnline };