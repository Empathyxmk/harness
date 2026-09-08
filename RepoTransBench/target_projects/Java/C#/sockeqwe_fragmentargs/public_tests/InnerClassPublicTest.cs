using Xunit;

namespace ProjectName.PublicTests.Processor
{
    public class InnerClassPublicTest
    {
        [Fact]
        public void TestInnerClassAccess_PublicVariant()
        {
            var outer = new OuterClassPublic(21);
            var inner = new OuterClassPublic.InnerClass(outer);
            Assert.Equal(105, inner.MultiplyOuterField(5));
        }

        public class OuterClassPublic
        {
            private int value;
            public OuterClassPublic(int value) { this.value = value; }
            public class InnerClass
            {
                private readonly OuterClassPublic _outer;
                public InnerClass(OuterClassPublic outer) { _outer = outer; }
                public int MultiplyOuterField(int by) { return _outer.value * by; }
            }
        }
    }
}