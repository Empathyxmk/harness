using System;
using Xunit;

namespace Casidiablo.MultiDex.Tests.Original
{
    public class MultiDexStandaloneTest
    {
        [Fact]
        public void TestPrivateConstructorCoverage()
        {
            try
            {
                var ctor = typeof(MultiDex).GetConstructor(System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic, null, Type.EmptyTypes, null);
                ctor.Invoke(null);
            }
            catch
            {
                // Ignore; only test private coverage
            }
        }

        [Fact]
        public void TestIsVMMultidexCapableEdgeCases()
        {
            Assert.False(MultiDex.IsVMMultidexCapable(""));
            Assert.False(MultiDex.IsVMMultidexCapable("abc.def"));
            Assert.True(MultiDex.IsVMMultidexCapable("3.10.99"));
        }
    }
}