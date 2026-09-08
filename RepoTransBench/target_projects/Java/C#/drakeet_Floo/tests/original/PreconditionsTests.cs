using Xunit;
using Drakeet.Floo;
using System;

public class PreconditionsTests
{
    [Fact]
    public void CheckNotNullThrows()
    {
        Assert.Throws<NullReferenceException>(() =>
        {
            Preconditions.CheckNotNull<object>(null, "err");
        });
    }

    [Fact]
    public void CheckNotNullNoThrow()
    {
        Preconditions.CheckNotNull("a", "err");
    }

    [Fact]
    public void CheckArgumentThrows()
    {
        Assert.Throws<ArgumentException>(() =>
        {
            Preconditions.CheckArgument(false, "arg error");
        });
    }

    [Fact]
    public void CheckArgumentNoThrow()
    {
        Preconditions.CheckArgument(true, "ok arg");
    }
}