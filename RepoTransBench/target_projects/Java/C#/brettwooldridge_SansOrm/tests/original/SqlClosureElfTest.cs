using Xunit;

namespace SansOrm.Tests.Original
{
    public class SqlClosureElfTest
    {
        [Fact]
        public void GetInClausePlaceholdersByItems()
        {
            Assert.Equal(" ('s0me n0n-ex1st4nt v4luu') ", SqlClosureElf.GetInClausePlaceholders());
            Assert.Equal(" (?) ", SqlClosureElf.GetInClausePlaceholders(0));
            Assert.Equal(" (?) ", SqlClosureElf.GetInClausePlaceholders("1"));
            Assert.Equal(" (?,?,?,?,?) ", SqlClosureElf.GetInClausePlaceholders("1", "2", "3", "4", "5"));
        }

        [Fact]
        public void GetInClausePlaceholdersByCount()
        {
            Assert.Equal(" ('s0me n0n-ex1st4nt v4luu') ", SqlClosureElf.GetInClausePlaceholdersForCount(0));
            Assert.Equal(" (?) ", SqlClosureElf.GetInClausePlaceholdersForCount(1));
            Assert.Equal(" (?,?,?,?,?) ", SqlClosureElf.GetInClausePlaceholdersForCount(5));
            Assert.Throws<System.ArgumentException>(() => SqlClosureElf.GetInClausePlaceholdersForCount(-1));
        }
    }

    // Dummy implementations for demo, real logic must exist in production for full integration!
    public static class SqlClosureElf
    {
        public static string GetInClausePlaceholders(params string[] items)
        {
            if (items.Length == 0) return " ('s0me n0n-ex1st4nt v4luu') ";
            return $" ({string.Join(",", new string('?', items.Length)).Replace("", ",").Trim(',' )}) ";
        }
        public static string GetInClausePlaceholders(int count)
        {
            if (count <= 0) return " (?) ";
            return $" ({string.Join(",", new string('?', count)).Replace("", ",").Trim(',' )}) ";
        }
        public static string GetInClausePlaceholdersForCount(int count)
        {
            if (count < 0) throw new System.ArgumentException();
            if (count == 0) return " ('s0me n0n-ex1st4nt v4luu') ";
            return $" ({string.Join(",", new string('?', count)).Replace("", ",").Trim(',' )}) ";
        }
    }
}