using System.Reflection;
using Xunit;

namespace DavidMoten.Geo.Tests
{
    public class GeoHashMinimalTest
    {
        [Fact]
        public void TestPrivateConstructor()
        {
            var ctor = typeof(GeoHash).GetConstructor(BindingFlags.NonPublic | BindingFlags.Instance, null, System.Type.EmptyTypes, null);
            Assert.NotNull(ctor);
            ctor.Invoke(null);
        }
    }
}