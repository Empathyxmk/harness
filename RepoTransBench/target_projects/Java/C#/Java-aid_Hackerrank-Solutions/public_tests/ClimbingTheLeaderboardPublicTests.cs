using Xunit;
using HackerrankSolutions;
using System.Collections.Generic;

public class ClimbingTheLeaderboardPublicTests
{
    [Fact]
    public void TestCustomCase1()
    {
        List<int> ranked = new List<int> { 120, 100, 100, 50, 40, 40, 20, 10 };
        List<int> player = new List<int> { 5, 25, 45, 60, 105, 130 };

        int[] expected = { 8, 6, 4, 4, 2, 1 };

        Assert.Equal(expected, ClimbingTheLeaderboard.ClimbingLeaderboard(ranked, player));
    }

    [Fact]
    public void TestCustomCase2()
    {
        List<int> ranked = new List<int> { 200, 180, 180, 170, 160, 160, 150, 140 };
        List<int> player = new List<int> { 130, 135, 150, 175, 190, 210 };

        int[] expected = { 9, 9, 7, 4, 2, 1 };

        Assert.Equal(expected, ClimbingTheLeaderboard.ClimbingLeaderboard(ranked, player));
    }
}