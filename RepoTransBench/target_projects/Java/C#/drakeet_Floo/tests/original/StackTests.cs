using Xunit;
using Drakeet.Floo;

public class StackTests
{
    [Fact]
    public void StatesAndResult()
    {
        var stack = new Stack();
        Assert.Equal(StackStates.STATE_CREATED, stack.GetState());
        stack.SetState(StackStates.STATE_INITED);
        Assert.Equal(StackStates.STATE_INITED, stack.GetState());

        stack.SetResult("result");
        Assert.Equal("result", stack.GetResult());
    }

    class Callback : IStackCallback
    {
        public bool Called = false;
        public void Run(Stack s)
        {
            Called = true;
            Assert.Same(stackRef, s);
        }
        public Stack stackRef;
    }

    [Fact]
    public void StackCallback()
    {
        var stack = new Stack();
        var cb = new Callback();
        cb.stackRef = stack;
        stack.SetCallback(cb);
        stack.OnResult();
        Assert.True(cb.Called);
    }
}