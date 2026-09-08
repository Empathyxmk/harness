using Xunit;
using Drakeet.Floo;

public class TargetTests
{
    [Fact]
    public void TargetConstructorsAndEquals()
    {
        var t1 = new Target("route", "activity");
        var t2 = new Target("route", "activity");
        var t3 = new Target("route2", "activity");
        Assert.Equal("route", t1.Route);
        Assert.Equal("activity", t1.TargetClass);
        Assert.Equal(t1, t2);
        Assert.NotEqual(t1, t3);
        Assert.NotEqual(t1, null);
        Assert.NotEqual(t1, new object());
        Assert.Equal(t1.GetHashCode(), t2.GetHashCode());
    }
}