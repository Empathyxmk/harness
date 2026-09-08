using Xunit;

namespace GoogleAuth.Tests
{
    public class HmacHashFunctionTest
    {
        [Fact]
        public void TestValueOf()
        {
            Assert.Equal(
                HmacHashFunction.ValueOf("HmacSHA1"), HmacHashFunction.ValueOf("HmacSHA1"));
            Assert.Equal(
                HmacHashFunction.ValueOf("HmacSHA256"), HmacHashFunction.ValueOf("HmacSHA256"));
            Assert.Equal(
                HmacHashFunction.ValueOf("HmacSHA512"), HmacHashFunction.ValueOf("HmacSHA512"));
        }

        [Fact]
        public void TestValuesArePresent()
        {
            string allNames = "";
            foreach (var fn in HmacHashFunction.Values())
            {
                allNames += fn.Name();
            }
            Assert.Contains("HmacSHA1", allNames);
            Assert.Contains("HmacSHA256", allNames);
            Assert.Contains("HmacSHA512", allNames);
        }
    }
}