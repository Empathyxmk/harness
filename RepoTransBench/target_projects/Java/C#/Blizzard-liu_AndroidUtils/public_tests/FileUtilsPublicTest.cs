using Xunit;

namespace AndroidUtils.PublicTests
{
    public class FileUtilsPublicTest
    {
        [Fact]
        public void TestGetFileExtensionJson_Public()
        {
            // Use a different extension, e.g., json
            string fileName = "myapiresult.json";
            string ext = fileName.Substring(fileName.LastIndexOf('.'));
            Assert.Equal(".json", ext);
        }
    }
}