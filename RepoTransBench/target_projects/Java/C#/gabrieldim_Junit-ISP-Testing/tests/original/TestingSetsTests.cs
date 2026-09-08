using System;
using System.Collections.Generic;
using Xunit;

public class TestingSetsTests
{
    // Test: Both sets are neither empty nor null; basic set difference with no overlap
    [Fact]
    public void TestSetDifference_NoOverlap_NonNull()
    {
        var set1 = new HashSet<int> { 1 };
        var set2 = new HashSet<int> { 2 };
        var result = TestingSets.SetDifference(new HashSet<int>(set1), set2);
        Assert.NotNull(result);
        Assert.Equal(set1, result);
    }

    // Test: set2 is empty - set1 unchanged
    [Fact]
    public void TestSetDifference_Set2Empty()
    {
        var set1 = new HashSet<int> { 3 };
        var set2 = new HashSet<int>();
        var result = TestingSets.SetDifference(new HashSet<int>(set1), set2);
        Assert.NotNull(result);
        Assert.Equal(set1, result);
    }

    // Test: set1 has elements, some overlap with set2
    [Fact]
    public void TestSetDifference_WithOverlap()
    {
        var set1 = new HashSet<int> { 1, 2, 3 };
        var set2 = new HashSet<int> { 2, 4 };
        var expected = new HashSet<int> { 1, 3 };

        var result = TestingSets.SetDifference(new HashSet<int>(set1), set2);
        Assert.Equal(expected, result);
    }

    // Test: set1 empty, set2 non-empty
    [Fact]
    public void TestSetDifference_Set1Empty_Set2NonEmpty()
    {
        var set1 = new HashSet<int>();
        var set2 = new HashSet<int> { 4 };
        var result = TestingSets.SetDifference(new HashSet<int>(set1), set2);
        Assert.Null(result);
    }

    // Test: set1 is null
    [Fact]
    public void TestSetDifference_Set1Null()
    {
        var set2 = new HashSet<int> { 1 };
        Assert.Throws<NullReferenceException>(() => TestingSets.SetDifference<int>(null, set2));
    }

    // Test: set2 is null
    [Fact]
    public void TestSetDifference_Set2Null()
    {
        var set1 = new HashSet<int> { 2 };
        Assert.Throws<NullReferenceException>(() => TestingSets.SetDifference<int>(set1, null));
    }

    // Test: both sets are null
    [Fact]
    public void TestSetDifference_BothNull()
    {
        Assert.Throws<NullReferenceException>(() => TestingSets.SetDifference<int>(null, null));
    }

    // Test: set1 has elements, ALL elements in set2 (should become empty, thus return null)
    [Fact]
    public void TestSetDifference_AllElementsRemoved()
    {
        var set1 = new HashSet<int> { 10, 20 };
        var set2 = new HashSet<int> { 10, 20, 30 };
        var result = TestingSets.SetDifference(new HashSet<int>(set1), set2);
        Assert.Null(result);
    }

    // Test: set1 is empty, set2 is empty
    [Fact]
    public void TestSetDifference_BothEmpty()
    {
        var set1 = new HashSet<int>();
        var set2 = new HashSet<int>();
        var result = TestingSets.SetDifference(new HashSet<int>(set1), set2);
        Assert.Null(result);
    }

    // Test: set1 and set2 identical
    [Fact]
    public void TestSetDifference_IdenticalSets()
    {
        var set1 = new HashSet<int> { 100, 200 };
        var set2 = new HashSet<int> { 100, 200 };
        var result = TestingSets.SetDifference(new HashSet<int>(set1), set2);
        Assert.Null(result);
    }
}