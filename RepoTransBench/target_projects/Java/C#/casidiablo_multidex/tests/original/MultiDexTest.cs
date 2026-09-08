using Xunit;

namespace Casidiablo.MultiDex.Tests.Original
{
    public class MultiDexTest
    {
        [Fact]
        public void TestVersionCheck()
        {
            Assert.False(MultiDex.IsVMMultidexCapable(null));
            Assert.False(MultiDex.IsVMMultidexCapable("-1.32.54"));
            Assert.False(MultiDex.IsVMMultidexCapable("1.32.54"));
            Assert.False(MultiDex.IsVMMultidexCapable("1.32"));
            Assert.False(MultiDex.IsVMMultidexCapable("2.0"));
            Assert.False(MultiDex.IsVMMultidexCapable("2.000.1254"));
            Assert.True(MultiDex.IsVMMultidexCapable("2.1.1254"));
            Assert.True(MultiDex.IsVMMultidexCapable("2.1"));
            Assert.True(MultiDex.IsVMMultidexCapable("2.2"));
            Assert.True(MultiDex.IsVMMultidexCapable("2.1.0000"));
            Assert.True(MultiDex.IsVMMultidexCapable("2.2.0000"));
            Assert.True(MultiDex.IsVMMultidexCapable("002.0001.0010"));
            Assert.True(MultiDex.IsVMMultidexCapable("3.0"));
            Assert.True(MultiDex.IsVMMultidexCapable("3.0.0"));
            Assert.True(MultiDex.IsVMMultidexCapable("3.0.1"));
            Assert.True(MultiDex.IsVMMultidexCapable("3.1.0"));
            Assert.True(MultiDex.IsVMMultidexCapable("03.1.132645"));
            Assert.True(MultiDex.IsVMMultidexCapable("03.2"));
        }
    }
}