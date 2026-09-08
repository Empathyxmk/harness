using Xunit;
using Drakeet.Floo;

public class UrlsPublicTests
{
    [Fact]
    public void IsWebSchemeWithHttp_Public()
    {
        Assert.True(Urls.IsWebScheme("http://floo.io"));
    }

    [Fact]
    public void IsWebSchemeWithCustomScheme_Public()
    {
        Assert.False(Urls.IsWebScheme("notweb://example.org"));
    }

    [Fact]
    public void Combine_Public()
    {
        Assert.Equal("foo://bar/baz", Urls.Combine("foo://bar", "baz"));
    }
}