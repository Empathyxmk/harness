const { getSnapshotUrl, isOnline } = require('../src/ipCameraUtils');

describe('getSnapshotUrl', () => {
    it('should build the snapshot URL correctly', () => {
        expect(getSnapshotUrl('http://host', 'cam1')).toBe('http://host/camera/cam1/snapshot');
    });

    it('should throw if baseUrl is missing', () => {
        expect(() => getSnapshotUrl(null, 'cam1')).toThrow('Missing arguments');
    });

    it('should throw if cameraId is missing', () => {
        expect(() => getSnapshotUrl('http://host', null)).toThrow('Missing arguments');
    });

    it('should throw on invalid baseUrl', () => {
        expect(() => getSnapshotUrl('ftp://host', 'cam1')).toThrow('Invalid baseUrl');
        expect(() => getSnapshotUrl('host', 'cam1')).toThrow('Invalid baseUrl');
    });
});

describe('isOnline', () => {
    it('should return true for connected camera', () => {
        expect(isOnline({ connected: true, lastPing: 1234 })).toBe(true);
    });

    it('should return false if not connected', () => {
        expect(isOnline({ connected: false, lastPing: 1234 })).toBe(false);
    });

    it('should return false for missing connected', () => {
        expect(isOnline({})).toBe(false);
        expect(isOnline(undefined)).toBe(false);
        expect(isOnline(null)).toBe(false);
    });
});