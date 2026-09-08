using System.Collections.Generic;
using Xunit;

namespace Skydoves.PreferenceRoom.OriginalTests
{
    public class Preference_UserDevice
    {
        private static Preference_UserDevice _instance;
        private Dictionary<string, object> prefs = new();

        public static Preference_UserDevice GetInstance()
            => _instance ??= new Preference_UserDevice();

        public void PutVersion(string version) => prefs["version"] = version;
        public string GetVersion() => prefs.ContainsKey("version") ? (string)prefs["version"] : null;

        public void PutUuid(string uuid)
        {
            prefs["uuid"] = SecurityUtils.Encrypt(uuid);
            prefs["decrypted_uuid"] = uuid;
        }
        public string GetUuid() => prefs.ContainsKey("decrypted_uuid") ? (string)prefs["decrypted_uuid"] : null;

        public string VersionKeyName() => "version";
        public string GetEntityName() => "UserDevice";
    }

    public static class SecurityUtils
    {
        public static string Encrypt(string value) => "ENCRYPTED_" + value;
    }

    public class DeviceEntityTests
    {
        private Preference_UserDevice device;

        private const string version = "1.0.0.0";
        private const string uuid = "00001234-0000-0000-0000-000123456789";

        public DeviceEntityTests()
        {
            device = Preference_UserDevice.GetInstance();
        }

        [Fact]
        public void VersionTest()
        {
            device.PutVersion(version);
            Assert.Equal(version, device.GetVersion());
        }

        [Fact]
        public void SecurityTest()
        {
            device.PutUuid(uuid);
            Assert.Equal(uuid, device.GetUuid());
            Assert.Equal("ENCRYPTED_" + uuid, SecurityUtils.Encrypt(uuid));
        }
    }
}