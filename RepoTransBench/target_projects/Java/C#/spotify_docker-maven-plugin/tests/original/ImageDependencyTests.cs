using System.IO;
using Newtonsoft.Json.Linq;
using Xunit;

namespace OriginalTests
{
    public class ImageDependencyTests
    {
        public static readonly string IMAGE_INFO_LOCATION =
            "META-INF/docker/com.spotify.docker.it/with-many-modules-a/image-info.json";

        [Fact]
        public void TestImageAvailable()
        {
            using (var stream = typeof(ImageDependencyTests).Assembly.GetManifestResourceStream(IMAGE_INFO_LOCATION))
            {
                var jsonNode = JObject.Parse(new StreamReader(stream).ReadToEnd());
                Assert.Equal("with-many-modules-a", (string)jsonNode["image"]);
            }
        }
    }
}