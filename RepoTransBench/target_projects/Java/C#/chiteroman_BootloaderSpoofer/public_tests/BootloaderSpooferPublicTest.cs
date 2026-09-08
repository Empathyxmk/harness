using Xunit;
using BootloaderSpoofer;

namespace BootloaderSpooferTests.Public
{
    public class BootloaderSpooferPublicTest
    {
        [Fact]
        public void TestToggleSpoofState()
        {
            var bs = new BootloaderSpoofer.BootloaderSpoofer();
            // Sequence: spoof, reset, spoof
            bs.Spoof();
            Assert.True(bs.IsSpoofed());
            Assert.Equal("Spoofed", bs.Status());
            bs.Reset();
            Assert.False(bs.IsSpoofed());
            Assert.Equal("Not spoofed", bs.Status());
            bs.Spoof();
            Assert.True(bs.IsSpoofed());
            Assert.Equal("Spoofed", bs.Status());
        }

        [Fact]
        public void TestMultipleReset()
        {
            var bs = new BootloaderSpoofer.BootloaderSpoofer();
            // Try resetting before spoofing, then after spoofing
            bs.Reset(); // should remain Not spoofed
            Assert.False(bs.IsSpoofed());
            Assert.Equal("Not spoofed", bs.Status());
            bs.Spoof();
            Assert.True(bs.IsSpoofed());
            bs.Reset();
            bs.Reset(); // should stay Not spoofed after two resets
            Assert.False(bs.IsSpoofed());
            Assert.Equal("Not spoofed", bs.Status());
        }

        [Fact]
        public void TestAlternatingSpoofAndReset()
        {
            var bs = new BootloaderSpoofer.BootloaderSpoofer();
            // Spoof -> Reset -> Spoof -> Reset
            bs.Spoof();
            Assert.True(bs.IsSpoofed());
            bs.Reset();
            Assert.False(bs.IsSpoofed());
            bs.Spoof();
            Assert.True(bs.IsSpoofed());
            bs.Reset();
            Assert.False(bs.IsSpoofed());
            Assert.Equal("Not spoofed", bs.Status());
        }

        [Fact]
        public void TestRepeatedResetWithoutSpoof()
        {
            var bs = new BootloaderSpoofer.BootloaderSpoofer();
            bs.Reset();
            bs.Reset();
            // Never spoofed
            Assert.False(bs.IsSpoofed());
            Assert.Equal("Not spoofed", bs.Status());
            // Now spoof and test again
            bs.Spoof();
            Assert.True(bs.IsSpoofed());
            bs.Reset();
            Assert.False(bs.IsSpoofed());
        }
    }
}