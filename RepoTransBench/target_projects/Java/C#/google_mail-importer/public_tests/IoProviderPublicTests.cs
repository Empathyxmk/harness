using System.IO;
using Xunit;

namespace GoogleMailImporter.PublicTests
{
    public class IoProviderPublicTests
    {
        [Fact]
        public void TestDifferentReadAllReturnsStream()
        {
            var testString = "PublicTestContent123";
            var input = new MemoryStream(System.Text.Encoding.UTF8.GetBytes(testString));
            var bytes = IoProvider.ReadAll(input);
            Assert.Equal(testString, System.Text.Encoding.UTF8.GetString(bytes));
        }
    }

    public static class IoProvider
    {
        public static byte[] ReadAll(Stream input)
        {
            using (var ms = new MemoryStream())
            {
                input.CopyTo(ms);
                return ms.ToArray();
            }
        }
    }
}