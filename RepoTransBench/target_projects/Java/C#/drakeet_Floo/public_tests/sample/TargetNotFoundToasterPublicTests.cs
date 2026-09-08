using Xunit;

public class TargetNotFoundToaster
{
    public bool OnTargetNotFound(object context, string uri, object extras, int? flags)
    {
        return true;
    }
}

public class TargetNotFoundToasterPublicTests
{
    private object context;
    private object extras;
    private TargetNotFoundToaster handler;
    private string uri;

    public TargetNotFoundToasterPublicTests()
    {
        context = new object();
        extras = new object();
        handler = new TargetNotFoundToaster();
        uri = "another://public-missing";
    }

    [Fact]
    public void OnTargetNotFound_AlwaysReturnsTrue_Public()
    {
        var result = handler.OnTargetNotFound(context, uri, extras, null);
        Assert.True(result);
    }
}