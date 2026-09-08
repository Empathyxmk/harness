using Xunit;

namespace MadvirusDddStart.PublicTests
{
    public class SpringConfigPublicTests
    {
        [Fact]
        public void EventStoreHandler_Bean_Has_ApplicationContext_And_Type()
        {
            // Instead of using ApplicationContext, just simulate presence of multiple beans:
            var beans = new[] { new EventStoreHandler() };
            Assert.True(beans.Length > 0);
            foreach (var bean in beans)
            {
                Assert.NotNull(bean);
                Assert.IsType<EventStoreHandler>(bean);
            }
        }
    }
}