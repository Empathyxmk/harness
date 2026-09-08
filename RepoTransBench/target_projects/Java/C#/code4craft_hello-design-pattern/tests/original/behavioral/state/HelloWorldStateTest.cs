using Xunit;
using System.Reflection;

namespace HelloDesignPattern.Tests.behavioral.state
{
    public class HelloWorldStateTest
    {
        [Fact]
        public void TestInitialState()
        {
            var ctx = new HelloWorldStateContext();
            Assert.NotNull(ctx);
            Assert.NotNull(ctx.ToString());
        }

        [Fact]
        public void TestStateTransitionsManual()
        {
            var ctx = new HelloWorldStateContext();
            MethodInfo nextState = typeof(HelloWorldStateContext).GetMethod("NextState", BindingFlags.NonPublic | BindingFlags.Instance);
            Assert.NotNull(nextState);

            // transition through all states several times
            for (int i = 0; i < 5; i++)
            {
                try
                {
                    nextState.Invoke(ctx, null);
                }
                catch (TargetInvocationException e)
                {
                    Assert.False(true, "Reflection NextState should not throw: " + e.InnerException?.Message ?? e.Message);
                }
            }
        }
    }
}