using OpenJfxJavafxMavenPlugin.Model;
using Xunit;

namespace OpenJfxJavafxMavenPlugin.PublicTests.Model
{
    public class RuntimePathOptionPublicTest
    {
        [Fact]
        public void TestValueOfDifferentData()
        {
            Assert.Equal(RuntimePathOption.MODULEPATH, (RuntimePathOption)System.Enum.Parse(typeof(RuntimePathOption), "MODULEPATH"));
            Assert.Equal(RuntimePathOption.CLASSPATH, (RuntimePathOption)System.Enum.Parse(typeof(RuntimePathOption), "CLASSPATH"));
        }

        [Fact]
        public void TestValuesArrayLengthAndContentDifferentOrder()
        {
            var values = (RuntimePathOption[])System.Enum.GetValues(typeof(RuntimePathOption));
            Assert.True(values.Length >= 2);
            Assert.True(values[0] != values[1]);
        }
    }
}