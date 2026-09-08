using Xunit;
using Moq;
using Drakeet.Floo;

public class WebHandler
{
    // The handler is a stub for the test, will mimic intended behaviors below
    public virtual bool OnTargetNotFound(MockContext context, string uri, object extras, int? flags)
    {
        if (uri.StartsWith("http://") || uri.StartsWith("https://"))
        {
            // Simulate intent logic and context.startActivity(intent)
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

// Minimal mockable Context stub
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

public class WebHandlerTests
{
    private MockContext context;
    private object extras;
    private WebHandler handler;
    private string webUri;
    private string nonWebUri;

    public WebHandlerTests()
    {
        context = new MockContext();
        extras = new object();
        handler = new WebHandler();
        webUri = "https://example.com";
        nonWebUri = "foo://bar";
    }

    [Fact]
    public void OnTargetNotFound_WebScheme_WithoutFlags()
    {
        var result = handler.OnTargetNotFound(context, webUri, extras, null);
        Assert.True(result);
        Assert.NotNull(context.LastStartedIntent);
        Assert.Equal(webUri, context.LastStartedIntent.Url);
    }

    [Fact]
    public void OnTargetNotFound_WebScheme_WithFlags()
    {
        var result = handler.OnTargetNotFound(context, webUri, extras, 0x10000000); // Corresponds to FLAG_ACTIVITY_NEW_TASK
        Assert.True(result);
        Assert.NotNull(context.LastStartedIntent);
        Assert.Equal(webUri, context.LastStartedIntent.Url);
        Assert.Equal(0x10000000, context.LastStartedIntent.Flags);
    }

    [Fact]
    public void OnTargetNotFound_NonWebScheme()
    {
        var result = handler.OnTargetNotFound(context, nonWebUri, extras, null);
        Assert.False(result);
        Assert.Null(context.LastStartedIntent);
    }
}