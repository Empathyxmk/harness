using Xunit;
using Drakeet.Floo;

public class InvalidJsonExceptionPublicTests
{
    [Fact]
    public void Message_Public()
    {
        var e = new InvalidJsonException("New message for public test");
        Assert.Equal("New message for public test", e.Message);
    }

    [Fact]
    public void NullMessage_Public()
    {
        var e = new InvalidJsonException(null);
        Assert.Null(e.Message);
    }
}