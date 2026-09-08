using OpenJfxJavafxMavenPlugin.Model;
using Xunit;

namespace OpenJfxJavafxMavenPlugin.Tests.Original.Model
{
    public class RuntimePathOptionTest
    {
        [Fact]
        public void TestEnumValues()
        {
            Assert.Equal(RuntimePathOption.CLASSPATH, (RuntimePathOption)System.Enum.Parse(typeof(RuntimePathOption), "CLASSPATH"));
            Assert.Equal(RuntimePathOption.MODULEPATH, (RuntimePathOption)System.Enum.Parse(typeof(RuntimePathOption), "MODULEPATH"));
            Assert.Equal(2, System.Enum.GetValues(typeof(RuntimePathOption)).Length);
        }
    }
}