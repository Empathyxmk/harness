using Xunit;
using Drakeet.Floo;

public class UrlsTests
{
    [Fact]
    public void IsRemoteUrl()
    {
        Assert.True(Urls.IsRemoteUrl("http://example.com"));
        Assert.True(Urls.IsRemoteUrl("https://secure.com"));
        Assert.False(Urls.IsRemoteUrl("file://local.txt"));
        Assert.False(Urls.IsRemoteUrl("content://file"));
        Assert.False(Urls.IsRemoteUrl(null));
        Assert.False(Urls.IsRemoteUrl(""));
    }

    [Fact]
    public void IsLocalUrl()
    {
        Assert.True(Urls.IsLocalUrl("file://localfile.txt"));
        Assert.True(Urls.IsLocalUrl("content://local"));
        Assert.False(Urls.IsLocalUrl("http://remote.net"));
        Assert.False(Urls.IsLocalUrl("https://secure.com"));
        Assert.False(Urls.IsLocalUrl(null));
        Assert.False(Urls.IsLocalUrl(""));
    }
}