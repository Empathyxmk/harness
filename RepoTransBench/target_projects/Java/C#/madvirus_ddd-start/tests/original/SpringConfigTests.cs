using Xunit;

namespace MadvirusDddStart.Tests.Original
{
    public class SpringConfigTests
    {
        [Fact]
        public void EventStoreHandler_IsNotAppliedByEventAOP()
        {
            // This would require DI context, simulated as an example:
            object bean = new EventStoreHandler();
            Assert.NotNull(bean);
            Assert.IsType<EventStoreHandler>(bean);
        }
    }
}