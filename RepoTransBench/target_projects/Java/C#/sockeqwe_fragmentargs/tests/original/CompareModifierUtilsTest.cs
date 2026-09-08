using System.Collections.Generic;
using Xunit;
using Moq;

namespace ProjectName.Tests.Original.Processor
{
    public static class ModifierUtils
    {
        // For demo: Simulate Java visibility: -1 = less visible, 0 = same, 1 = more visible
        public static int CompareModifierVisibility(HashSet<string> aModifiers, HashSet<string> bModifiers)
        {
            static int Visibility(HashSet<string> modifiers)
            {
                if (modifiers.Contains("public"))
                    return 3;
                if (modifiers.Contains("protected"))
                    return 2;
                if (modifiers.Contains("private"))
                    return 0;
                return 1; // default
            }
            int diff = Visibility(aModifiers) - Visibility(bModifiers);
            if (diff == 0) return 0;
            return diff > 0 ? 1 : -1;
        }
    }

    public class CompareModifierUtilsTest
    {
        HashSet<string> aModifiers, bModifiers;

        public CompareModifierUtilsTest()
        {
            aModifiers = new HashSet<string>();
            bModifiers = new HashSet<string>();
        }

        [Fact]
        public void APublicBNot()
        {
            aModifiers.Add("public");
            bModifiers.Add("private");
            Assert.Equal(-1, ModifierUtils.CompareModifierVisibility(aModifiers, bModifiers));
        }

        [Fact]
        public void ADefaultBNot()
        {
            bModifiers.Add("private");
            Assert.Equal(-1, ModifierUtils.CompareModifierVisibility(aModifiers, bModifiers));
        }

        [Fact]
        public void AProtectedBNot()
        {
            aModifiers.Add("protected");
            bModifiers.Add("private");
            Assert.Equal(-1, ModifierUtils.CompareModifierVisibility(aModifiers, bModifiers));
        }

        [Fact]
        public void BPublicANot()
        {
            bModifiers.Add("public");
            aModifiers.Add("private");
            Assert.Equal(1, ModifierUtils.CompareModifierVisibility(aModifiers, bModifiers));
        }

        [Fact]
        public void BDefaultANot()
        {
            aModifiers.Add("private");
            Assert.Equal(1, ModifierUtils.CompareModifierVisibility(aModifiers, bModifiers));
        }

        [Fact]
        public void BProtectedANot()
        {
            aModifiers.Add("private");
            bModifiers.Add("protected");
            Assert.Equal(1, ModifierUtils.CompareModifierVisibility(aModifiers, bModifiers));
        }

        [Fact]
        public void SamePrivate()
        {
            aModifiers.Add("private");
            bModifiers.Add("private");
            Assert.Equal(0, ModifierUtils.CompareModifierVisibility(aModifiers, bModifiers));
        }

        [Fact]
        public void SameProtected()
        {
            aModifiers.Add("private");
            bModifiers.Add("private");
            Assert.Equal(0, ModifierUtils.CompareModifierVisibility(aModifiers, bModifiers));
        }

        [Fact]
        public void SameDefault()
        {
            Assert.Equal(0, ModifierUtils.CompareModifierVisibility(aModifiers, bModifiers));
        }

        [Fact]
        public void SamePublic()
        {
            aModifiers.Add("public");
            bModifiers.Add("public");
            Assert.Equal(0, ModifierUtils.CompareModifierVisibility(aModifiers, bModifiers));
        }
    }
}