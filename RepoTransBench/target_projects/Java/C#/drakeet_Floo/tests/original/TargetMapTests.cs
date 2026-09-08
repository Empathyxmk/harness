using Xunit;
using Drakeet.Floo;

public class TargetMapTests
{
    [Fact]
    public void PutAndGet()
    {
        var map = new TargetMap();
        var t1 = new Target("route1", "activity1");
        map.Put("key", t1);

        Assert.True(map.ContainsKey("key"));
        Assert.Equal(t1, map.Get("key"));
    }

    [Fact]
    public void Remove()
    {
        var map = new TargetMap();
        var t1 = new Target("route2", "activity2");
        map.Put("rm", t1);
        map.Remove("rm");
        Assert.False(map.ContainsKey("rm"));
    }

    [Fact]
    public void IsEmpty()
    {
        var map = new TargetMap();
        Assert.True(map.IsEmpty());
        map.Put("a", new Target("a", "a"));
        map.Remove("a");
        Assert.True(map.IsEmpty());
    }
}