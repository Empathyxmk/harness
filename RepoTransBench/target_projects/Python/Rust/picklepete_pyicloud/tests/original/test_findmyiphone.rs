// Test for iterating over device collections and validating fields.

struct Device {
    data: std::collections::HashMap<&'static str, Option<&'static str>>,
}

impl Device {
    fn new(name: &'static str) -> Self {
        let mut h = std::collections::HashMap::new();
        // Simulate all required keys/fields per test
        for key in [
            "canWipeAfterLock", "baUUID", "wipeInProgress", "lostModeEnabled",
            "activationLocked", "passcodeLength", "deviceStatus", "features", "lowPowerMode",
            "rawDeviceModel", "id", "isLocating", "modelDisplayName", "lostTimestamp",
            "batteryLevel", "locationEnabled", "locFoundEnabled", "fmlyShare", "lostModeCapable",
            "wipedTimestamp", "deviceDisplayName", "audioChannels", "locationCapable",
            "batteryStatus", "trackingInfo", "name", "isMac", "thisDevice", "deviceClass",
            "deviceModel", "maxMsgChar", "darkWake", "remoteWipe"
        ] {
            // For test coverage, simulate all as Some("whatever") except wipedTimestamp, trackingInfo, remoteWipe
            h.insert(key, match key {
                "wipedTimestamp" | "trackingInfo" | "remoteWipe" => None,
                _ => Some("val")
            });
        }
        h.insert("name", Some(name));
        Device { data: h }
    }

    fn get(&self, key: &str) -> Option<&Option<&str>> {
        self.data.get(key)
    }
}

#[test]
fn test_devices() {
    let mut devices = vec![];
    // Simulate 13 devices with "DeviceN" as name
    for i in 1..=13 {
        devices.push(Device::new("Device"));
    }
    assert_eq!(devices.len(), 13);

    for device in &devices {
        for &field in [
            "canWipeAfterLock","baUUID","wipeInProgress","lostModeEnabled","activationLocked",
            "passcodeLength","deviceStatus","features","lowPowerMode","rawDeviceModel","id",
            "isLocating","modelDisplayName","lostTimestamp","batteryLevel","locationEnabled",
            "locFoundEnabled","fmlyShare","lostModeCapable","deviceDisplayName",
            "audioChannels","locationCapable","batteryStatus","name","isMac","thisDevice",
            "deviceClass","deviceModel","maxMsgChar","darkWake"
        ].iter() {
            assert!(device.get(field).unwrap().is_some());
            assert_ne!(device.get(field), Some(&None));
        }
        // These must be None
        for &field in ["wipedTimestamp", "trackingInfo", "remoteWipe"].iter() {
            assert!(device.get(field).is_some());
            assert!(device.get(field).unwrap().is_none());
        }
    }
}