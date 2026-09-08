using Xunit;
using HackerrankSolutions;
using System.Collections.Generic;

public class ClimbingTheLeaderboardTests
{
    [Fact]
    public void TestTypicalCase()
    {
        int[] scores = { 100, 100, 50, 40, 40, 20, 10 };
        int[] alice = { 5, 25, 50, 120 };
        int[] expected = { 6, 4, 2, 1 };
        Assert.Equal(expected, ClimbingTheLeaderboard.ClimbingLeaderboard(scores, alice));
    }

    [Fact]
    public void TestAllScoresSame()
    {
        int[] scores = { 100, 100, 100 };
        int[] alice = { 50, 100, 101 };
        int[] expected = { 2, 1, 1 };
        Assert.Equal(expected, ClimbingTheLeaderboard.ClimbingLeaderboard(scores, alice));
    }

    [Fact]
    public void TestAliceAllLower()
    {
        int[] scores = { 60, 30, 10 };
        int[] alice = { 5, 3 };
        int[] expected = { 4, 4 };
        Assert.Equal(expected, ClimbingTheLeaderboard.ClimbingLeaderboard(scores, alice));
    }

    [Fact]
    public void TestAliceAllHigher()
    {
        int[] scores = { 40, 20, 10 };
        int[] alice = { 50 };
        int[] expected = { 1 };
        Assert.Equal(expected, ClimbingTheLeaderboard.ClimbingLeaderboard(scores, alice));
    }

    [Fact]
    public void TestSingleElementScores()
    {
        int[] scores = { 100 };
        int[] alice = { 100, 101, 99 };
        int[] expected = { 1, 1, 2 };
        Assert.Equal(expected, ClimbingTheLeaderboard.ClimbingLeaderboard(scores, alice));
    }

    [Fact]
    public void TestBinarySearch()
    {
        int[] a = { 100, 90, 80, 70, 70, 60 };
        Assert.Equal(3, ClimbingTheLeaderboard.BinarySearch(a, 70));
        Assert.Equal(2, ClimbingTheLeaderboard.BinarySearch(a, 85));
        Assert.Equal(1, ClimbingTheLeaderboard.BinarySearch(a, 95));
        Assert.Equal(-1, ClimbingTheLeaderboard.BinarySearch(a, 50));
    }

    [Fact]
    public void TestMainTypicalCase()
    {
        string input = "7\n100 100 50 40 40 20 10\n4\n5 25 50 120\n";
        string output = CaptureConsoleOutput(() =>
        {
            Console.SetIn(new System.IO.StringReader(input));
            ClimbingTheLeaderboard.Main(new string[0]);
        });
        Assert.Contains("1", output);
        Assert.Contains("6", output);
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