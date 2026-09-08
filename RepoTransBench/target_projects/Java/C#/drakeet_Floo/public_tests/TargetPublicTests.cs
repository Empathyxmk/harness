using Xunit;

public class Target
{
    private string url;
    private string targetClass;

    public Target(string url, string targetClass)
    {
        this.url = url;
        this.targetClass = targetClass;
    }

    public string GetUrl() => url;
    public string GetTargetClass() => targetClass;
    public void SetUrl(string url) => this.url = url;
}

public class TargetPublicTests
{
    [Fact]
    public void CreateAndGetUrl_Public()
    {
        var target = new Target("foo://bar", "SomeClass");
        Assert.Equal("foo://bar", target.GetUrl());
        Assert.Equal("SomeClass", target.GetTargetClass());
    }

    [Fact]
    public void SetUrl_Public()
    {
        var target = new Target("foo://baz", "OtherClass");
        target.SetUrl("foo://changed");
        Assert.Equal("foo://changed", target.GetUrl());
    }
}