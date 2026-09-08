using Xunit;
using System.Collections.Generic;

public class Stack<T>
{
    private readonly Stack<T> _list = new();
    public void Push(T item)
    {
        _list.Push(item);
    }
    public T Pop()
    {
        return _list.Count == 0 ? default : _list.Pop();
    }
    public bool IsEmpty()
    {
        return _list.Count == 0;
    }
}

public class StackPublicTests
{
    private Stack<int> stack;

    public StackPublicTests()
    {
        stack = new Stack<int>();
    }

    [Fact]
    public void PushThenPop_Public()
    {
        stack.Push(99);
        stack.Push(42);
        Assert.Equal(42, stack.Pop());
        Assert.Equal(99, stack.Pop());
    }

    [Fact]
    public void IsEmpty_Public()
    {
        Assert.True(stack.IsEmpty());
        stack.Push(1);
        Assert.False(stack.IsEmpty());
    }
}