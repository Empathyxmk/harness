using Xunit;
using System.Collections.Generic;

public class TargetMap
{
    private readonly Dictionary<string, string> _map = new();

    public void Put(string key, string value)
    {
        _map[key] = value;
    }

    public string Get(string key)
    {
        return _map.TryGetValue(key, out var v) ? v : null;
    }
}

public class TargetMapPublicTests
{
    [Fact]
    public void PutAndGet_Public()
    {
        var map = new TargetMap();
        map.Put("/my/path", "targetValue");
        Assert.Equal("targetValue", map.Get("/my/path"));
    }

    [Fact]
    public void GetNonExistingKey_Public()
    {
        var map = new TargetMap();
        Assert.Null(map.Get("/no/such/key"));
    }
}