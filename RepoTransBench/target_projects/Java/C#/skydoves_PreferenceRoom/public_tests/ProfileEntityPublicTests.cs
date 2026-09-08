using Xunit;

namespace Skydoves.PreferenceRoom.PublicTests
{
    public class Profile
    {
        public string Name { get; }
        public string Email { get; }
        public string Phone { get; private set; }

        public Profile(string context, string name, string email) { Name = name; Email = email; }
        public void SetPhone(string phone) => Phone = phone;
        public string GetPhone() => Phone;
    }

    public class ProfileEntityPublicTests
    {
        private Profile publicProfile;

        public ProfileEntityPublicTests()
        {
            publicProfile = new Profile("context", "public_name", "public@email.org");
            publicProfile.SetPhone("123987456");
        }

        [Fact]
        public void TestNamePublic()
        {
            Assert.Equal("public_name", publicProfile.Name);
        }

        [Fact]
        public void TestEmailPublic()
        {
            Assert.Equal("public@email.org", publicProfile.Email);
        }

        [Fact]
        public void TestPhonePublic()
        {
            Assert.Equal("123987456", publicProfile.GetPhone());
        }
    }
}