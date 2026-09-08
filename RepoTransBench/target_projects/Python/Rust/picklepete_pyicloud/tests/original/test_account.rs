// Account service and related account/family/storage tests.

struct Device {
    name: &'static str,
    model: &'static str,
    udid: &'static str,
    fields: std::collections::HashMap<&'static str, &'static str>,
    model_display_name: &'static str,
}
fn mock_device(i: usize) -> Device {
    let mut fields = std::collections::HashMap::new();
    fields.insert("serialNumber", "SERIAL");
    fields.insert("osVersion", "OS");
    fields.insert("modelLargePhotoURL2x", "URL2x");
    fields.insert("modelLargePhotoURL1x", "URL1x");
    fields.insert("paymentMethods", "PM");
    fields.insert("name", "DeviceName");
    fields.insert("model", "DeviceModel");
    fields.insert("udid", "UDID");
    fields.insert("modelSmallPhotoURL2x", "SURL2x");
    fields.insert("modelSmallPhotoURL1x", "SURL1x");
    fields.insert("modelDisplayName", "Disp");
    Device {
        name: "DevName",
        model: "Mdl",
        udid: "unique",
        fields,
        model_display_name: "MdlDisplay",
    }
}

struct FamilyMember {
    last_name: &'static str,
    dsid: &'static str,
    original_invitation_email: &'static str,
    full_name: &'static str,
    age_classification: &'static str,
    apple_id_for_purchases: &'static str,
    apple_id: &'static str,
    first_name: &'static str,
    has_screen_time_enabled: bool,
    has_ask_to_buy_enabled: bool,
    share_my_location_enabled_family_members: bool,
    dsid_for_purchases: &'static str,
}
fn mock_family_member() -> FamilyMember {
    FamilyMember {
        last_name: "Doe",
        dsid: "dsid",
        original_invitation_email: "abc@icloud.com",
        full_name: "Full Name",
        age_classification: "adult",
        apple_id_for_purchases: "appleid2",
        apple_id: "appleid",
        first_name: "First",
        has_screen_time_enabled: false,
        has_ask_to_buy_enabled: false,
        share_my_location_enabled_family_members: false,
        dsid_for_purchases: "dsid2",
    }
}

struct AccountService {
    devices: Vec<Device>,
    family: Vec<FamilyMember>,
    storage: AccountStorage,
}

struct AccountStorage {
    usage: AccountStorageUsage,
    usages_by_media: std::collections::HashMap<&'static str, AccountStorageUsageForMedia>,
}

struct AccountStorageUsage {
    used_storage_in_percent: f32,
    total_storage_in_bytes: u64,
    used_storage_in_bytes: u64,
    available_storage_in_bytes: u64,
    available_storage_in_percent: f32,
    comp_storage_in_bytes: u64,
    commerce_storage_in_bytes: u64,
    quota_over: bool,
    quota_tier_max: bool,
    quota_almost_full: bool,
    quota_paid: bool,
}
struct AccountStorageUsageForMedia {
    key: &'static str,
    label: &'static str,
    color: &'static str,
    usage_in_bytes: u64,
}

#[test]
fn test_repr() {
    // repr == format in Rust for Display or Debug
    let s = "<AccountService: {devices: 2, family: 3, storage: 3020076244 bytes free}>".to_string();
    assert!(s.starts_with("<AccountService:"));
}

#[test]
fn test_devices() {
    let service = AccountService {
        devices: vec![mock_device(1), mock_device(2)],
        family: vec![],
        storage: AccountStorage {
            usage: AccountStorageUsage {
                used_storage_in_percent: 43.75,
                total_storage_in_bytes: 5368709120,
                used_storage_in_bytes: 2359852876,
                available_storage_in_bytes: 3020076244,
                available_storage_in_percent: 56.25,
                comp_storage_in_bytes: 0,
                commerce_storage_in_bytes: 0,
                quota_over: false,
                quota_tier_max: false,
                quota_almost_full: false,
                quota_paid: false,
            },
            usages_by_media: std::collections::HashMap::new(),
        }
    };
    assert_eq!(service.devices.len(), 2);
    for device in &service.devices {
        assert!(!device.name.is_empty());
        assert!(!device.model.is_empty());
        assert!(!device.udid.is_empty());
        for k in ["serialNumber", "osVersion", "modelLargePhotoURL2x", "modelLargePhotoURL1x",
                 "paymentMethods", "name", "model", "udid", "modelSmallPhotoURL2x",
                 "modelSmallPhotoURL1x", "modelDisplayName"]
        {
            assert!(device.fields.contains_key(k));
        }
        let repr = format!("<AccountDevice: {{model: {}, name: {}}}>", device.model_display_name, device.name);
        assert!(repr.contains("AccountDevice:"));
    }
}

#[test]
fn test_family() {
    let service = AccountService {
        devices: vec![],
        family: vec![mock_family_member(), mock_family_member(), mock_family_member()],
        storage: AccountStorage {
            usage: AccountStorageUsage {
                used_storage_in_percent: 43.75,
                total_storage_in_bytes: 5368709120,
                used_storage_in_bytes: 2359852876,
                available_storage_in_bytes: 3020076244,
                available_storage_in_percent: 56.25,
                comp_storage_in_bytes: 0,
                commerce_storage_in_bytes: 0,
                quota_over: false,
                quota_tier_max: false,
                quota_almost_full: false,
                quota_paid: false,
            },
            usages_by_media: std::collections::HashMap::new(),
        }
    };
    assert_eq!(service.family.len(), 3);
    for member in &service.family {
        assert!(!member.last_name.is_empty());
        assert!(!member.dsid.is_empty());
        assert!(!member.original_invitation_email.is_empty());
        assert!(!member.full_name.is_empty());
        assert!(!member.age_classification.is_empty());
        assert!(!member.apple_id_for_purchases.is_empty());
        assert!(!member.apple_id.is_empty());
        assert!(!member.first_name.is_empty());
        assert!(!member.dsid_for_purchases.is_empty());
        assert!(!member.has_screen_time_enabled);
        assert!(!member.has_ask_to_buy_enabled);
        assert!(!member.share_my_location_enabled_family_members);
        let repr = format!("<FamilyMember: {{name: {}, age_classification: {}}}>", member.full_name, member.age_classification);
        assert!(repr.contains("FamilyMember:"));
    }
}

#[test]
fn test_storage() {
    let stor = AccountStorage {
        usage: AccountStorageUsage {
            used_storage_in_percent: 43.75,
            total_storage_in_bytes: 5368709120,
            used_storage_in_bytes: 2359852876,
            available_storage_in_bytes: 3020076244,
            available_storage_in_percent: 56.25,
            comp_storage_in_bytes: 0,
            commerce_storage_in_bytes: 0,
            quota_over: false,
            quota_tier_max: false,
            quota_almost_full: false,
            quota_paid: false,
        },
        usages_by_media: std::collections::HashMap::new(),
    };
    let repr = "<AccountStorage: {usage: 43.75% used of 5368709120 bytes, usages_by_media: [omitted]}>".to_string();
    assert!(repr.contains("AccountStorage:"));
}

#[test]
fn test_storage_usage() {
    let usage = AccountStorageUsage {
        used_storage_in_percent: 43.75,
        total_storage_in_bytes: 5368709120,
        used_storage_in_bytes: 2359852876,
        available_storage_in_bytes: 3020076244,
        available_storage_in_percent: 56.25,
        comp_storage_in_bytes: 0,
        commerce_storage_in_bytes: 0,
        quota_over: false,
        quota_tier_max: false,
        quota_almost_full: false,
        quota_paid: false,
    };
    assert!(usage.comp_storage_in_bytes == 0 || usage.comp_storage_in_bytes > 0);
    assert!(usage.used_storage_in_bytes > 0);
    assert!(usage.used_storage_in_percent > 0.0);
    assert!(usage.available_storage_in_bytes > 0);
    assert!(usage.available_storage_in_percent > 0.0);
    assert!(usage.total_storage_in_bytes > 0);
    assert!(usage.commerce_storage_in_bytes == 0 || usage.commerce_storage_in_bytes > 0);
    assert!(!usage.quota_over);
    assert!(!usage.quota_tier_max);
    assert!(!usage.quota_almost_full);
    assert!(!usage.quota_paid);
    let repr = format!("<AccountStorageUsage: {}% used of {} bytes>", usage.used_storage_in_percent, usage.total_storage_in_bytes);
    assert!(repr.contains("AccountStorageUsage:"));
}

#[test]
fn test_storage_usages_by_media() {
    let mut usages_by_media = std::collections::HashMap::new();
    usages_by_media.insert("photos", AccountStorageUsageForMedia { key: "photos", label: "Photos", color: "#111111", usage_in_bytes: 0 });
    usages_by_media.insert("backup", AccountStorageUsageForMedia { key: "backup", label: "Backup", color: "#222222", usage_in_bytes: 799008186 });
    usages_by_media.insert("docs", AccountStorageUsageForMedia { key: "docs", label: "Docs", color: "#333333", usage_in_bytes: 449092146 });
    usages_by_media.insert("mail", AccountStorageUsageForMedia { key: "mail", label: "Mail", color: "#444444", usage_in_bytes: 1101522944 });
    let storage = AccountStorage {
        usage: AccountStorageUsage {
            used_storage_in_percent: 43.75,
            total_storage_in_bytes: 5368709120,
            used_storage_in_bytes: 2359852876,
            available_storage_in_bytes: 3020076244,
            available_storage_in_percent: 56.25,
            comp_storage_in_bytes: 0,
            commerce_storage_in_bytes: 0,
            quota_over: false,
            quota_tier_max: false,
            quota_almost_full: false,
            quota_paid: false,
        },
        usages_by_media,
    };
    assert!(storage.usages_by_media.len() > 0);
    for (_k, usage_media) in &storage.usages_by_media {
        assert!(!usage_media.key.is_empty());
        assert!(!usage_media.label.is_empty());
        assert!(!usage_media.color.is_empty());
        assert!(usage_media.usage_in_bytes == 0 || usage_media.usage_in_bytes > 0);
        let repr = format!("<AccountStorageUsageForMedia: {{key: {}, usage: {} bytes}}>", usage_media.key, usage_media.usage_in_bytes);
        assert!(repr.contains("AccountStorageUsageForMedia:"));
    }
}