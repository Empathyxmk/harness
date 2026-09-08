using Xunit;
using HackerrankSolutions;

public class TripleSumTests
{
    [Fact]
    public void TestTypicalCase()
    {
        int[] a = { 1, 3, 5 };
        int[] b = { 2, 3 };
        int[] c = { 1, 2, 3 };
        long expected = 8;
        Assert.Equal(expected, TripleSum.Triplets(a, b, c));
    }

    [Fact]
    public void TestDuplicateValues()
    {
        int[] a = { 1, 3, 5, 3 };
        int[] b = { 2, 3, 3 };
        int[] c = { 1, 2, 3, 1 };
        long expected = 8;
        Assert.Equal(expected, TripleSum.Triplets(a, b, c));
    }

    [Fact]
    public void TestAllZeros()
    {
        int[] a = { 0, 0, 0 };
        int[] b = { 0, 0 };
        int[] c = { 0, 0 };
        long expected = 1;
        Assert.Equal(expected, TripleSum.Triplets(a, b, c));
    }

    [Fact]
    public void TestEmptyArrays()
    {
        int[] a = new int[0];
        int[] b = new int[0];
        int[] c = new int[0];
        long expected = 0;
        Assert.Equal(expected, TripleSum.Triplets(a, b, c));
    }

    [Fact]
    public void TestRemoveDuplicates()
    {
        int[] arr = { 1, 1, 2, 2, 3, 3, 3 };
        var res = TripleSum.RemoveDuplicates(arr);
        Assert.Equal(3, res.Length);
        Assert.All(res, x => Assert.Contains(x, new[] { 1, 2, 3 }));
    }

    [Fact]
    public void TestGetValidIndex()
    {
        int[] arr = { 1, 2, 3, 4, 5 };
        Assert.Equal(2, TripleSum.GetValidIndex(arr, 3));
        Assert.Equal(4, TripleSum.GetValidIndex(arr, 6));
        Assert.Equal(-1, TripleSum.GetValidIndex(arr, 0));
        Assert.Equal(0, TripleSum.GetValidIndex(new int[] { 2 }, 2));
    }

    [Fact]
    public void TestMainExampleInput()
    {
        string input = "3 2 3\n1 3 5\n2 3\n1 2 3\n";
        string output = CaptureConsoleOutput(() =>
        {
            Console.SetIn(new System.IO.StringReader(input));
            TripleSum.Main(new string[0]);
        });
        Assert.Contains("8", output);
    }

    [Fact]
    public void TestMainWithEmptyArrays()
    {
        string input = "0 0 0\n\n\n\n";
        string output = CaptureConsoleOutput(() =>
        {
            Console.SetIn(new System.IO.StringReader(input));
            TripleSum.Main(new string[0]);
        });
        Assert.Contains("0", output);
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