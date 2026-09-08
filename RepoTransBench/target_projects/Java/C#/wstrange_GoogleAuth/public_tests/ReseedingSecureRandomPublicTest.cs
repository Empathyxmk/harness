using System;
using System.Reflection;
using Xunit;

namespace GoogleAuth.PublicTests
{
    public class ReseedingSecureRandomPublicTest
    {
        [Fact]
        public void TestDefaultConstructorAndNextBytes_public()
        {
            var random = new ReseedingSecureRandom();
            byte[] bytes = new byte[12];
            random.NextBytes(bytes);
            Assert.NotNull(bytes);
            Assert.Equal(12, bytes.Length);
        }

        [Fact]
        public void TestConstructorWithAlgorithm_public()
        {
            var random = new ReseedingSecureRandom("SHA1PRNG");
            byte[] bytes = new byte[8];
            random.NextBytes(bytes);
            Assert.NotNull(bytes);
            Assert.Equal(8, bytes.Length);
        }

        [Fact]
        public void TestConstructorWithAlgorithmAndProvider_invalidProvider_public()
        {
            var ex = Assert.Throws<GoogleAuthenticatorException>(() =>
            {
                var _ = new ReseedingSecureRandom("SHA1PRNG", "NON_EXISTENT_PROVIDER");
            });
            Assert.Contains("provider", ex.Message, StringComparison.OrdinalIgnoreCase);
        }

        [Fact]
        public void TestConstructorWithNullAlgorithm_public()
        {
            var ex = Assert.Throws<ArgumentException>(() =>
            {
                var _ = new ReseedingSecureRandom(null as string);
            });
        }

        [Fact]
        public void TestConstructorWithNullProvider_public()
        {
            var ex = Assert.Throws<ArgumentException>(() =>
            {
                var _ = new ReseedingSecureRandom("SHA1PRNG", null);
            });
        }

        [Fact]
        public void TestForceReseed_public()
        {
            var random = new ReseedingSecureRandom();
            // Set count via reflection to a higher value to simulate reseed trigger
            FieldInfo countField = typeof(ReseedingSecureRandom).GetField("count", BindingFlags.NonPublic | BindingFlags.Instance);
            Assert.NotNull(countField);
            var countValue = countField.GetValue(random) as AtomicInteger;
            Assert.NotNull(countValue);
            countValue.Set(2_000_001);

            byte[] bytes = new byte[7];
            random.NextBytes(bytes);
            Assert.NotNull(bytes);
            Assert.Equal(7, bytes.Length);
        }
    }
}