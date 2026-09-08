using Xunit;

namespace MadvirusDddStart.Tests.Original
{
    public class TypeDescriptorTests
    {
        [Fact]
        public void PrimitiveTypesAreSingletons()
        {
            Assert.NotNull(TypeDescriptor.BOOLEAN_TYPE);
            Assert.NotNull(TypeDescriptor.BYTE_TYPE);
            Assert.NotNull(TypeDescriptor.CHAR_TYPE);
            Assert.NotNull(TypeDescriptor.DOUBLE_TYPE);
            Assert.NotNull(TypeDescriptor.FLOAT_TYPE);
            Assert.NotNull(TypeDescriptor.INT_TYPE);
        }
    }
}