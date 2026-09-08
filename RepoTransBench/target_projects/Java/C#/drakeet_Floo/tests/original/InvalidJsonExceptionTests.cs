using Xunit;
using Drakeet.Floo;
using System;

public class InvalidJsonExceptionTests
{
    [Fact]
    public void ConstructorWithMessageAndThrowable()
    {
        var t = new Exception("test");
        var ex = new InvalidJsonException("message", t);
        Assert.Contains("message", ex.Message);
        Assert.Equal(t, ex.InnerException);
    }
}