using System.Collections.Generic;
using Xunit;

namespace ProjectName.Tests.Original.Processor
{
    public static class ModifierUtils
    {
        public static bool IsDefaultModifier(HashSet<string> modifiers)
        {
            // default if not public/protected/private
            foreach (var mod in modifiers)
            {
                if (mod == "public" || mod == "private" || mod == "protected")
                    return false;
            }
            return true;
        }
    }

    public class ModifierUtilsDefaultModifierTest
    {
        [Fact]
        public void IsDefaultModifierTest()
        {
            var modifiers = new HashSet<string> { "public" };
            Assert.False(ModifierUtils.IsDefaultModifier(modifiers));

            modifiers.Clear();
            modifiers.Add("private");
            Assert.False(ModifierUtils.IsDefaultModifier(modifiers));

            modifiers.Clear();
            modifiers.Add("protected");
            Assert.False(ModifierUtils.IsDefaultModifier(modifiers));

            modifiers.Clear();
            modifiers.Add("final");
            modifiers.Add("static");
            Assert.True(ModifierUtils.IsDefaultModifier(modifiers));
        }
    }
}