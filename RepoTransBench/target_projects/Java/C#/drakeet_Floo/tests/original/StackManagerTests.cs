using Xunit;
using Drakeet.Floo;

public class StackManagerTests
{
    [Fact]
    public void PushAndPeek()
    {
        var stackManager = new StackManager();
        var stack = new Stack();
        stackManager.Push(stack);

        Assert.Same(stack, stackManager.Peek());
    }

    [Fact]
    public void PopAndEmpty()
    {
        var stackManager = new StackManager();
        var stack = new Stack();
        stackManager.Push(stack);
        var popped = stackManager.Pop();
        Assert.Same(stack, popped);
        Assert.Null(stackManager.Peek());
    }

    [Fact]
    public void EmptyPop()
    {
        var stackManager = new StackManager();
        Assert.Null(stackManager.Pop());
    }

    [Fact]
    public void IsNotEmpty()
    {
        var stackManager = new StackManager();
        Assert.False(stackManager.IsNotEmpty());
        stackManager.Push(new Stack());
        Assert.True(stackManager.IsNotEmpty());
    }
}