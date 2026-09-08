using Xunit;

namespace GoogleAuth.Tests
{
    public class KeyRepresentationTest
    {
        [Fact]
        public void TestValues()
        {
            var reps = KeyRepresentation.Values();
            Assert.NotNull(reps);
            Assert.True(reps.Length > 0);
        }

        [Fact]
        public void TestValueOf()
        {
            Assert.Equal(KeyRepresentation.BASE32, KeyRepresentation.ValueOf("BASE32"));
            Assert.Equal(KeyRepresentation.BASE64, KeyRepresentation.ValueOf("BASE64"));
        }
    }
}