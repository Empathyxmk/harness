using System.IO;
using Xunit;

namespace GoogleMailImporter.PublicTests.Local
{
    public class JavaxMailStoragePublicTests
    {
        [Fact]
        public void TestCreateFlagDifferentInput()
        {
            var flags = new EmailFlags();
            flags.Add("DRAFT");
            var msg = new MimeMessage();
            JavaxMailStorage.AddFlags(msg, flags);
            Assert.True(msg.Flags.Contains("DRAFT"));
        }
    }

    // Dummies for compilation only
    public class EmailFlags : HashSet<string>
    {
        public static string DRAFT = "DRAFT";
    }
    public class MimeMessage
    {
        public EmailFlags Flags { get; } = new EmailFlags();
    }
    public static class JavaxMailStorage
    {
        public static void AddFlags(MimeMessage msg, EmailFlags flags)
        {
            foreach (var flag in flags)
                msg.Flags.Add(flag);
        }
    }
}