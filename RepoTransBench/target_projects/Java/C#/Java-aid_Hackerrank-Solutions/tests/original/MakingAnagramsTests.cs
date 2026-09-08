using Xunit;
using HackerrankSolutions;

public class MakingAnagramsTests
{
    [Fact]
    public void TestTypicalCase()
    {
        string a = "abc";
        string b = "cde";
        Assert.Equal(4, MakingAnagrams.NumberNeeded(a, b));
    }

    [Fact]
    public void TestIdenticalStrings()
    {
        string a = "aabbcc";
        string b = "aabbcc";
        Assert.Equal(0, MakingAnagrams.NumberNeeded(a, b));
    }

    [Fact]
    public void TestAllDifferent()
    {
        string a = "abc";
        string b = "def";
        Assert.Equal(6, MakingAnagrams.NumberNeeded(a, b));
    }

    [Fact]
    public void TestEmptyA()
    {
        string a = "";
        string b = "xyz";
        Assert.Equal(3, MakingAnagrams.NumberNeeded(a, b));
    }

    [Fact]
    public void TestEmptyB()
    {
        string a = "xyz";
        string b = "";
        Assert.Equal(3, MakingAnagrams.NumberNeeded(a, b));
    }

    [Fact]
    public void TestBothEmpty()
    {
        Assert.Equal(0, MakingAnagrams.NumberNeeded("", ""));
    }

    [Fact]
    public void TestMainTypicalCase()
    {
        string input = "abc\ncde\n";
        string output = CaptureConsoleOutput(() =>
        {
            Console.SetIn(new System.IO.StringReader(input));
            MakingAnagrams.Main(new string[0]);
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