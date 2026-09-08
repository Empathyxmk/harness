using Xunit;
using Drakeet.Floo;

public class ChainTests
{
    class TestInterceptor : IInterceptor
    {
        public bool Called { get; private set; } = false;
        public void Intercept(Chain chain)
        {
            Called = true;
        }
    }

    [Fact]
    public void ChainSetAndProceed()
    {
        var chain = new Chain();
        var interceptor = new TestInterceptor();
        chain.SetInterceptor(interceptor);
        Assert.Same(interceptor, chain.GetInterceptor());

        chain.Proceed();
        Assert.True(interceptor.Called);
    }

    [Fact]
    public void ChainCallback()
    {
        var chain = new Chain();
        bool called = false;
        chain.SetCallback(() => { called = true; });
        chain.Callback();
        Assert.True(called);
    }

    [Fact]
    public void DefaultStates()
    {
        var chain = new Chain();
        Assert.Null(chain.GetInterceptor());
    }
}