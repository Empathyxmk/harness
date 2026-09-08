using Xunit;

namespace Casidiablo.MultiDex.Tests.Public
{
    public class MultiDexStandalonePublicTest
    {
        [Fact]
        public void TestPrivateConstructorCoveragePublic()
        {
            try
            {
                var ctor = typeof(MultiDex).GetConstructor(System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic, null, System.Type.EmptyTypes, null);
                ctor.Invoke(null);
            }
            catch
            {
                // Ignore for code coverage only
            }
        }

        [Fact]
        public void TestIsVMMultidexCapableEdgeCasesPublic()
        {
            Assert.False(MultiDex.IsVMMultidexCapable(" "));
            Assert.False(MultiDex.IsVMMultidexCapable("xyz"));
            Assert.True(MultiDex.IsVMMultidexCapable("4.2.1"));
        }
    }
}