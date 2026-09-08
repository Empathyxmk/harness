using Xunit;
using System.Collections.Generic;
using Drakeet.Floo;

public class StackManagerPublicTests
{
    [Fact]
    public void PushPop_Public()
    {
        var manager = new StackManager<string>();
        manager.Push("alpha");
        manager.Push("beta");
        Assert.Equal("beta", manager.Pop());
        Assert.Equal("alpha", manager.Pop());
    }

    [Fact]
    public void PopOnEmpty_Public()
    {
        var manager = new StackManager<string>();
        Assert.Null(manager.Pop());
    }
}