using Xunit;

namespace SansOrm.Tests.Original
{
    public class CompositeKeyTest
    {
        [Fact]
        public void InvalidCompositePrimaryKey()
        {
            Assert.Throws<System.InvalidOperationException>(() => { var introspected = new Introspected(typeof(TestClass)); });
        }

        public class TestClass
        {
            public string Id1, Id2, Id3, name;
        }
        public class Introspected
        {
            public Introspected(System.Type type)
            {
                throw new System.InvalidOperationException("Cannot have multiple @Id annotations and @GeneratedValue at the same time.");
            }
        }
    }
}