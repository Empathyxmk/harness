const { getSnapshotUrl, isOnline } = require('../src/ipCameraUtils');

describe('getSnapshotUrl - PUBLIC', () => {
    it('should build the snapshot URL correctly with different data', () => {
        expect(getSnapshotUrl('https://example.com', 'cam42')).toBe('https://example.com/camera/cam42/snapshot');
    });

    it('should throw if baseUrl is empty string', () => {
        expect(() => getSnapshotUrl('', 'camx')).toThrow('Missing arguments');
    });

    it('should throw if cameraId is empty string', () => {
        expect(() => getSnapshotUrl('https://yoursite.org', '')).toThrow('Missing arguments');
    });

    it('should throw on invalid baseUrl (no protocol)', () => {
        expect(() => getSnapshotUrl('localhost:5555', 'mycam')).toThrow('Invalid baseUrl');
        expect(() => getSnapshotUrl('ftp://myhost', 'mycam')).toThrow('Invalid baseUrl');
    });
});

describe('isOnline - PUBLIC', () => {
    it('should return true for a different connected camera', () => {
        expect(isOnline({ connected: true, lastPing: 9876 })).toBe(true);
    });

    it('should return false if connected is false for different data', () => {
        expect(isOnline({ connected: false, lastPing: 0 })).toBe(false);
    });

    it('should return false for object with no "connected" field', () => {
        expect(isOnline({ foo: 'bar' })).toBe(false);
        expect(isOnline(undefined)).toBe(false);
        expect(isOnline(null)).toBe(false);
    });
});