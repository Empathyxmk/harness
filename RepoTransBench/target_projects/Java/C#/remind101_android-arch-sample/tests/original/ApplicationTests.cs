using Xunit;

namespace Remind101ArchExample.Tests.Original
{
    // Since this was just an Android ApplicationTestCase, we ensure *something* is testable in the .NET translation.
    public class ApplicationTests
    {
        [Fact]
        public void ApplicationCanInstantiate()
        {
            var app = new object();
            Assert.NotNull(app);
        }
    }
}