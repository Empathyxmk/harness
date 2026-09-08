using Xunit;
using Drakeet.Floo;

public class StackStatesPublicTests
{
    [Fact]
    public void StateValues_Public()
    {
        Assert.NotEqual(StackStates.ACTIVE, StackStates.PAUSED);
        Assert.NotEqual(StackStates.PAUSED, StackStates.DESTROYED);
    }

    [Fact]
    public void StateEquality_Public()
    {
        Assert.Equal("ACTIVE", StackStates.ACTIVE);
        Assert.NotEqual("PAUSED", StackStates.ACTIVE);
    }
}