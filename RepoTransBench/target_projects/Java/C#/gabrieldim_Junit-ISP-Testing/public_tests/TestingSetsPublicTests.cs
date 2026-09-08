using System;
using System.Collections.Generic;
using Xunit;

public class TestingSetsPublicTests
{
    // Public Test: Both sets are neither empty nor null; basic set difference with no overlap
    [Fact]
    public void TestSetDifference_NoOverlap_NonNull_Public()
    {
        var set1 = new HashSet<int> { 5 };
        var set2 = new HashSet<int> { 7 };
        var result = TestingSets.SetDifference(new HashSet<int>(set1), set2);
        Assert.NotNull(result);
        Assert.Equal(set1, result);
    }

    // Public Test: set2 is empty - set1 unchanged
    [Fact]
    public void TestSetDifference_Set2Empty_Public()
    {
        var set1 = new HashSet<int> { 9 };
        var set2 = new HashSet<int>();
        var result = TestingSets.SetDifference(new HashSet<int>(set1), set2);
        Assert.NotNull(result);
        Assert.Equal(set1, result);
    }

    // Public Test: set1 has elements, some overlap with set2
    [Fact]
    public void TestSetDifference_WithOverlap_Public()
    {
        var set1 = new HashSet<int> { 11, 13, 15 };
        var set2 = new HashSet<int> { 13, 17 };
        var expected = new HashSet<int> { 11, 15 };
        var result = TestingSets.SetDifference(new HashSet<int>(set1), set2);
        Assert.Equal(expected, result);
    }

    // Public Test: set1 empty, set2 non-empty
    [Fact]
    public void TestSetDifference_Set1Empty_Set2NonEmpty_Public()
    {
        var set1 = new HashSet<int>();
        var set2 = new HashSet<int> { 21 };
        var result = TestingSets.SetDifference(new HashSet<int>(set1), set2);
        Assert.Null(result);
    }

    // Public Test: set1 is null
    [Fact]
    public void TestSetDifference_Set1Null_Public()
    {
        var set2 = new HashSet<int> { 22 };
        Assert.Throws<NullReferenceException>(() => TestingSets.SetDifference<int>(null, set2));
    }

    // Public Test: set2 is null
    [Fact]
    public void TestSetDifference_Set2Null_Public()
    {
        var set1 = new HashSet<int> { 42 };
        Assert.Throws<NullReferenceException>(() => TestingSets.SetDifference<int>(set1, null));
    }

    // Public Test: both sets are null
    [Fact]
    public void TestSetDifference_BothNull_Public()
    {
        Assert.Throws<NullReferenceException>(() => TestingSets.SetDifference<int>(null, null));
    }

    // Public Test: set1 has elements, ALL elements in set2 (should become empty, thus return null)
    [Fact]
    public void TestSetDifference_AllElementsRemoved_Public()
    {
        var set1 = new HashSet<int> { 101, 202 };
        var set2 = new HashSet<int> { 202, 101, 303 };
        var result = TestingSets.SetDifference(new HashSet<int>(set1), set2);
        Assert.Null(result);
    }

    // Public Test: set1 is empty, set2 is empty
    [Fact]
    public void TestSetDifference_BothEmpty_Public()
    {
        var set1 = new HashSet<int>();
        var set2 = new HashSet<int>();
        var result = TestingSets.SetDifference(new HashSet<int>(set1), set2);
        Assert.Null(result);
    }

    // Public Test: set1 and set2 identical
    [Fact]
    public void TestSetDifference_IdenticalSets_Public()
    {
        var set1 = new HashSet<int> { 333, 444 };
        var set2 = new HashSet<int> { 444, 333 };
        var result = TestingSets.SetDifference(new HashSet<int>(set1), set2);
        Assert.Null(result);
    }
}