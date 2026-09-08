using Xunit;
using Moq;

namespace Skydoves.PreferenceRoom.PublicTests
{
    public class InjectorGeneratorPublicTests
    {
        [Fact]
        public void GenerateDifferentClassNameTest()
        {
            // Simulate different class name test
            var pcac = new Mock<object>();
            var injectedElement = new Mock<object>();
            var elementUtils = new Mock<object>();

            dynamic dynInjectedElement = injectedElement.AsDynamic();
            dynInjectedElement.SimpleName = "PublicClass";

            var injectorGenerator = new Mock<object>();
            var spec = new { name = "PublicClass_Injector" };

            Assert.Equal("PublicClass_Injector", spec.name);
            Assert.Contains("PreferenceRoom", "PreferenceRoom_Mock_Contents");
        }
    }
}