using Xunit;
using Drakeet.Floo;

public class PreconditionsPublicTests
{
    [Fact]
    public void CheckNotNull_NonNull_Public()
    {
        string s = "not null";
        Assert.Same(s, Preconditions.CheckNotNull(s));
    }

    [Fact]
    public void CheckNotNull_Null_Public()
    {
        Assert.Throws<NullReferenceException>(() =>
        {
            Preconditions.CheckNotNull<string>(null);
        });
    }
}