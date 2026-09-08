using Xunit;
using HackerrankSolutions;

public class StringsMakingAnagramsTests
{
    [Fact]
    public void TestTypicalCase()
    {
        string first = "cde";
        string second = "abc";
        Assert.Equal(4, StringsMakingAnagrams.NumberNeeded(first, second));
    }

    [Fact]
    public void TestReversedInputs()
    {
        string first = "abc";
        string second = "cde";
        Assert.Equal(4, StringsMakingAnagrams.NumberNeeded(first, second));
    }

    [Fact]
    public void TestIdentical()
    {
        string first = "abcd";
        string second = "abcd";
        Assert.Equal(0, StringsMakingAnagrams.NumberNeeded(first, second));
    }

    [Fact]
    public void TestEmptyA()
    {
        string first = "";
        string second = "aaa";
        Assert.Equal(3, StringsMakingAnagrams.NumberNeeded(first, second));
    }

    [Fact]
    public void TestEmptyB()
    {
        string first = "aaa";
        string second = "";
        Assert.Equal(3, StringsMakingAnagrams.NumberNeeded(first, second));
    }

    [Fact]
    public void TestBothEmpty()
    {
        Assert.Equal(0, StringsMakingAnagrams.NumberNeeded("", ""));
    }

    [Fact]
    public void TestMainTypicalCase()
    {
        string input = "cde\nabc\n";
        string output = CaptureConsoleOutput(() =>
        {
            Console.SetIn(new System.IO.StringReader(input));
            StringsMakingAnagrams.Main(new string[0]);
        });
        Assert.EndsWith("4", output.Trim());
    }

    private string CaptureConsoleOutput(Action action)
    {
        var currentOut = Console.Out;
        using (var sw = new System.IO.StringWriter())
        {
            Console.SetOut(sw);
            action();
            Console.SetOut(currentOut);
            return sw.ToString().Trim();
        }
    }
}