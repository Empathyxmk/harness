using Xunit;

namespace Casidiablo.MultiDex.Tests.Public
{
    public class MultiDexPublicTest
    {
        [Fact]
        public void TestVersionCheckPublic()
        {
            Assert.False(MultiDex.IsVMMultidexCapable("0.9"));
            Assert.False(MultiDex.IsVMMultidexCapable("1.999.9999"));
            Assert.False(MultiDex.IsVMMultidexCapable("2.0.0"));
            Assert.False(MultiDex.IsVMMultidexCapable("2.0.1"));

            Assert.True(MultiDex.IsVMMultidexCapable("2.10"));
            Assert.True(MultiDex.IsVMMultidexCapable("2.1.1"));
            Assert.True(MultiDex.IsVMMultidexCapable("4.0"));
            Assert.True(MultiDex.IsVMMultidexCapable("10.2"));
            Assert.True(MultiDex.IsVMMultidexCapable("2.1.1.5"));
            Assert.True(MultiDex.IsVMMultidexCapable("2.2.12345"));
            Assert.True(MultiDex.IsVMMultidexCapable("05.5.5"));

            Assert.True(MultiDex.IsVMMultidexCapable("002.001.0001"));
            Assert.False(MultiDex.IsVMMultidexCapable("2.0.9999"));
            Assert.False(MultiDex.IsVMMultidexCapable("2.0.0000"));
            Assert.True(MultiDex.IsVMMultidexCapable("3.0.42"));
        }
    }
}