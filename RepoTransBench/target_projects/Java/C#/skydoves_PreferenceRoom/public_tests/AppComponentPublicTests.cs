using Xunit;

namespace Skydoves.PreferenceRoom.PublicTests
{
    // Simplified Profile class for public test
    public class Profile
    {
        public string Name { get; }
        public string Email { get; }
        public Profile(string context, string name, string email)
        {
            Name = name;
            Email = email;
        }
    }

    public class AppComponentPublicTests
    {
        private Profile publicProfile;

        public AppComponentPublicTests()
        {
            // Use a "public" suffix
            publicProfile = new Profile("context", "public_test_user", "public@email.com");
        }

        [Fact]
        public void TestProfileNameIsSetPublic()
        {
            Assert.Equal("public_test_user", publicProfile.Name);
        }

        [Fact]
        public void TestProfileEmailIsSetPublic()
        {
            Assert.Equal("public@email.com", publicProfile.Email);
        }
    }
}