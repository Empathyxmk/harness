using Xunit;
using BootloaderSpoofer;

namespace BootloaderSpooferTests.Original
{
    public class BootloaderSpooferTest
    {
        [Fact]
        public void TestInitialStatus()
        {
            var bs = new BootloaderSpoofer.BootloaderSpoofer();
            Assert.False(bs.IsSpoofed());
            Assert.Equal("Not spoofed", bs.Status());
        }

        [Fact]
        public void TestSpoofSetsSpoofed()
        {
            var bs = new BootloaderSpoofer.BootloaderSpoofer();
            bs.Spoof();
            Assert.True(bs.IsSpoofed());
            Assert.Equal("Spoofed", bs.Status());
        }

        [Fact]
        public void TestReset()
        {
            var bs = new BootloaderSpoofer.BootloaderSpoofer();
            bs.Spoof();
            bs.Reset();
            Assert.False(bs.IsSpoofed());
            Assert.Equal("Not spoofed", bs.Status());
        }

        [Fact]
        public void TestMultipleSpoof()
        {
            var bs = new BootloaderSpoofer.BootloaderSpoofer();
            bs.Spoof();
            bs.Spoof(); // Should not change state or throw
            Assert.True(bs.IsSpoofed());
        }
    }
}