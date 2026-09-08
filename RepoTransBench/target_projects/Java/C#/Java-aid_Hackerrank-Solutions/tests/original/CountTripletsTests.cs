using Xunit;
using HackerrankSolutions;
using System.Collections.Generic;
using System.Linq;

public class CountTripletsTests
{
    [Fact]
    public void TestTypicalCase()
    {
        List<long> arr = new List<long> { 1L, 2L, 2L, 4L };
        long r = 2;
        long expected = 2;
        Assert.Equal(expected, CountTriplets.CountTripletsMethod(arr, r));
    }

    [Fact]
    public void TestAllOnesR1()
    {
        List<long> arr = new List<long> { 1L, 1L, 1L, 1L };
        long r = 1;
        Assert.Equal(4, CountTriplets.CountTripletsMethod(arr, r));
    }

    [Fact]
    public void TestNoTriplets()
    {
        List<long> arr = new List<long> { 1L, 2L, 4L, 8L };
        long r = 3;
        Assert.Equal(0, CountTriplets.CountTripletsMethod(arr, r));
    }

    [Fact]
    public void TestSingleElement()
    {
        List<long> arr = new List<long> { 7L };
        long r = 2;
        Assert.Equal(0, CountTriplets.CountTripletsMethod(arr, r));
    }

    [Fact]
    public void TestEmptyList()
    {
        List<long> arr = new List<long>();
        Assert.Equal(0, CountTriplets.CountTripletsMethod(arr, 2L));
    }

    [Fact]
    public void TestMainTypicalCase()
    {
        string input = "4 2\n1 2 2 4\n";
        string output = CaptureConsoleOutput(() =>
        {
            Console.SetIn(new System.IO.StringReader(input));
            CountTriplets.Main(new string[0]);
        });
        Assert.EndsWith("2", output.Trim());
    }

    [Fact]
    public void TestMainEmpty()
    {
        string input = "0 2\n";
        string output = CaptureConsoleOutput(() =>
        {
            Console.SetIn(new System.IO.StringReader(input));
            CountTriplets.Main(new string[0]);
        });
        Assert.EndsWith("0", output.Replace("\n", "").Trim());
    }

    private string CaptureConsoleOutput(Action action)
    {
        var currentOut = Console.Out;
        using (var sw = new System.IO.StringWriter())
        {
            Console.SetOut(sw);
            action();
            Console.SetOut(currentOut);
            return sw.ToString();
        }
    }
}