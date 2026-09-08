using System;
using System.Reflection;
using System.Threading;
using Xunit;

namespace GoogleAuth.Tests
{
    public class ReseedingSecureRandomTest
    {
        [Fact]
        public void TestDefaultConstructorAndNextBytes()
        {
            var random = new ReseedingSecureRandom();
            byte[] bytes = new byte[10];
            random.NextBytes(bytes);
            Assert.NotNull(bytes);
            Assert.True(bytes.Length > 0);
        }

        [Fact]
        public void TestConstructorWithAlgorithm()
        {
            var random = new ReseedingSecureRandom("SHA1PRNG");
            byte[] bytes = new byte[16];
            random.NextBytes(bytes);
            Assert.NotNull(bytes);
        }

        [Fact]
        public void TestConstructorWithAlgorithmAndProvider_invalidProvider()
        {
            var ex = Assert.Throws<GoogleAuthenticatorException>(() =>
            {
                var _ = new ReseedingSecureRandom("SHA1PRNG", "FAKE_PROVIDER");
            });
            Assert.Contains("provider", ex.Message, StringComparison.OrdinalIgnoreCase);
        }

        [Fact]
        public void TestConstructorWithNullAlgorithm()
        {
            var ex = Assert.Throws<ArgumentException>(() =>
            {
                var _ = new ReseedingSecureRandom(null as string);
            });
            // ok!
        }

        [Fact]
        public void TestConstructorWithNullProvider()
        {
            var ex = Assert.Throws<ArgumentException>(() =>
            {
                var _ = new ReseedingSecureRandom("SHA1PRNG", null);
            });
            // ok!
        }

        [Fact]
        public void TestForceReseed()
        {
            var random = new ReseedingSecureRandom();
            // Simulate crossing MAX_OPERATIONS by setting private count via reflection
            FieldInfo countField = typeof(ReseedingSecureRandom).GetField("count", BindingFlags.NonPublic | BindingFlags.Instance);
            Assert.NotNull(countField);
            var countValue = countField.GetValue(random) as AtomicInteger;
            Assert.NotNull(countValue);
            countValue.Set(1_000_001);

            byte[] bytes = new byte[5];
            random.NextBytes(bytes);
            Assert.NotNull(bytes);
        }
    }
}