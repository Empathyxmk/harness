using Xunit;

public class ChainPublicTests
{
    public abstract class Chain<T>
    {
        public abstract T Proceed(T input);
    }

    [Fact]
    public void ProceedReturnsData_Public()
    {
        var chain = new AnonymousStringChain();
        string result = chain.Proceed("hello");
        Assert.Equal("hello_public", result);
    }

    class AnonymousStringChain : Chain<string>
    {
        public override string Proceed(string input)
        {
            return input + "_public";
        }
    }

    [Fact]
    public void ProceedWithDifferentData_Public()
    {
        var chain = new AnonymousIntChain();
        int result = chain.Proceed(8);
        Assert.Equal(50, result);
    }

    class AnonymousIntChain : Chain<int>
    {
        public override int Proceed(int input)
        {
            return input + 42;
        }
    }
}