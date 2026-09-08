using Xunit;

namespace GoogleAuth.Tests
{
    public class GoogleAuthenticatorConfigTest
    {
        [Fact]
        public void TestDefaultConstructorAndGetters()
        {
            var config = new GoogleAuthenticatorConfig();
            Assert.True(config.WindowSize >= 0);
            Assert.True(config.CodeDigits >= 0);
            Assert.NotNull(config.KeyRepresentation);
            Assert.True(config.TimeStepSizeInMillis > 0);
            Assert.NotNull(config.HmacHashFunction);
            Assert.True(config.NumberOfScratchCodes >= 0);
            Assert.True(config.SecretBits >= 0);
        }

        [Fact]
        public void TestBuilder()
        {
            var builder = new GoogleAuthenticatorConfigBuilder();
            builder.SetWindowSize(4)
                .SetCodeDigits(7)
                .SetKeyRepresentation(KeyRepresentation.BASE64)
                .SetTimeStepSizeInMillis(654321L)
                .SetHmacHashFunction(HmacHashFunction.ValueOf("HmacSHA1"))
                .SetNumberOfScratchCodes(7)
                .SetSecretBits(160);

            var config = builder.Build();

            Assert.Equal(4, config.WindowSize);
            Assert.Equal(7, config.CodeDigits);
            Assert.Equal(KeyRepresentation.BASE64, config.KeyRepresentation);
            Assert.Equal(654321L, config.TimeStepSizeInMillis);
            Assert.Equal(HmacHashFunction.ValueOf("HmacSHA1"), config.HmacHashFunction);
            Assert.Equal(7, config.NumberOfScratchCodes);
            Assert.Equal(160, config.SecretBits);
        }
    }
}