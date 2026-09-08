using Xunit;

public class WebHandler
{
    public virtual bool OnTargetNotFound(MockContext context, string uri, object extras, int? flags)
    {
        if (uri.StartsWith("http://") || uri.StartsWith("https://"))
        {
            if (context != null)
            {
                context.StartActivity(new Intent { Url = uri, Flags = flags ?? 0 });
            }
            return true;
        }
        else
        {
            return false;
        }
    }
}

public class Intent
{
    public string Url { get; set; }
    public int Flags { get; set; }
}

public class MockContext
{
    public Intent LastStartedIntent { get; private set; }
    public int StartActivityCallCount { get; private set; }
    public virtual void StartActivity(Intent intent)
    {
        LastStartedIntent = intent;
        StartActivityCallCount++;
    }
}

public class WebHandlerPublicTests
{
    private MockContext context;
    private object extras;
    private WebHandler handler;
    private string webUri;
    private string nonWebUri;

    public WebHandlerPublicTests()
    {
        context = new MockContext();
        extras = new object();
        handler = new WebHandler();
        webUri = "http://public-example.org";
        nonWebUri = "customscheme://baz";
    }

    [Fact]
    public void OnTargetNotFound_WebScheme_WithoutFlags_Public()
    {
        var result = handler.OnTargetNotFound(context, webUri, extras, null);
        Assert.True(result);
        Assert.NotNull(context.LastStartedIntent);
    }

    [Fact]
    public void OnTargetNotFound_WebScheme_WithFlags_Public()
    {
        const int FLAG_ACTIVITY_REORDER_TO_FRONT = 0x20000;
        var result = handler.OnTargetNotFound(context, webUri, extras, FLAG_ACTIVITY_REORDER_TO_FRONT);
        Assert.True(result);
        Assert.NotNull(context.LastStartedIntent);
        Assert.Equal(webUri, context.LastStartedIntent.Url);
        Assert.Equal(FLAG_ACTIVITY_REORDER_TO_FRONT, context.LastStartedIntent.Flags);
    }

    [Fact]
    public void OnTargetNotFound_NonWebScheme_Public()
    {
        var result = handler.OnTargetNotFound(context, nonWebUri, extras, null);
        Assert.False(result);
        Assert.Null(context.LastStartedIntent);
    }
}