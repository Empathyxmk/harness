using Xunit;

namespace ProjectName.PublicTests.Processor
{
    public class ProtectedAccessPublicTest
    {
        [Fact]
        public void ProtectedFieldAccessTest_PublicVariant()
        {
            var dummy = new DummyProtectedObjectPublic();
            dummy.SetValue("barBaz");
            Assert.Equal("barBaz", dummy.GetValue());
        }

        public class DummyProtectedObjectPublic
        {
            protected string? field;
            public void SetValue(string val) => this.field = val;
            public string? GetValue() => this.field;
        }
    }
}