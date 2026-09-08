using Xunit;

namespace MadvirusDddStart.PublicTests
{
    public class TypeDescriptorPublicTests
    {
        [Fact]
        public void OtherPrimitiveTypesAreSingletons()
        {
            Assert.NotNull(TypeDescriptor.LONG_TYPE);
            Assert.NotNull(TypeDescriptor.SHORT_TYPE);
        }
    }
}