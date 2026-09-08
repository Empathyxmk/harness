using Xunit;

namespace ProjectName.PublicTests.Processor
{
    public class CompareModifierUtilsPublicTest
    {
        [Fact]
        public void CompareModifiers_PublicVariant()
        {
            var publicModifier = 0x0001;   // Java Public
            var privateModifier = 0x0002;  // Java Private
            var staticModifier = 0x0008;   // Java Static

            int combined = publicModifier | staticModifier;
            Assert.True((combined & publicModifier) != 0);
            Assert.True((combined & staticModifier) != 0);
            Assert.False((combined & privateModifier) != 0);
        }
    }
}