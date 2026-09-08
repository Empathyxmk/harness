using Xunit;

public static class URLs
{
    public static string Scheme() => "floo";
    public static string WEB = "https://m.drakeet.me/web";
    public static string NOT_REGISTERED = "floo://m.drakeet.me/not_registered";
}

public class URLsTests
{
    [Fact]
    public void SchemeIsFloo()
    {
        Assert.Equal("floo", URLs.Scheme());
    }

    [Fact]
    public void Constants()
    {
        Assert.Equal("https://m.drakeet.me/web", URLs.WEB);
        Assert.Equal("floo://m.drakeet.me/not_registered", URLs.NOT_REGISTERED);
    }
}