using Xunit;

public static class URLs
{
    public static string Scheme() => "floo";
    public static string WEB = "https://m.drakeet.me/web";
    public static string NOT_REGISTERED = "floo://m.drakeet.me/not_registered";
}

public class URLsPublicTests
{
    [Fact]
    public void SchemeIsFloo_Public()
    {
        Assert.Equal("floo", URLs.Scheme());
    }

    [Fact]
    public void Constants_Public()
    {
        Assert.NotEqual("https://not-public-url.com", URLs.WEB);
        Assert.NotEqual("floo://not/public", URLs.NOT_REGISTERED);
        Assert.StartsWith("https://", URLs.WEB);
        Assert.StartsWith("floo://", URLs.NOT_REGISTERED);
    }
}