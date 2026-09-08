using Xunit;

public class TargetNotFoundToaster
{
    public bool OnTargetNotFound(object context, string uri, object extras, int? flags)
    {
        return true;
    }
}

public class TargetNotFoundToasterTests
{
    private object context;
    private object extras;
    private TargetNotFoundToaster handler;
    private string uri;

    public TargetNotFoundToasterTests()
    {
        context = new object();
        extras = new object();
        handler = new TargetNotFoundToaster();
        uri = "some://missing";
    }

    [Fact]
    public void OnTargetNotFound_AlwaysReturnsTrue()
    {
        var result = handler.OnTargetNotFound(context, uri, extras, null);
        Assert.True(result);
    }
}