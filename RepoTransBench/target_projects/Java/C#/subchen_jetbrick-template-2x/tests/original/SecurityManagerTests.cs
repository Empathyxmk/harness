using System.Collections.Generic;
using Xunit;

namespace JetbrickTemplate.Tests.Original
{
    public class SecurityManagerTests : AbstractJetxTest
    {
        public override void InitializeEngine()
        {
            var nameList = new List<string>
            {
                "-java.io",
                "-java.lang.System",
                "-java.util.Date.<init>",
                "-java.lang.Integer.MAX_VALUE",
                "-java.lang.String.length",
                "-java.lang.CharSequence.length"
            };

            var securityManager = new JetSecurityManagerImpl();
            securityManager.SetNameList(nameList);

            engine.SetSecurityManager(securityManager);
        }

        [Fact]
        public void PkgAccess()
        {
            var ex = Assert.Throws<InterpretException>(() => Eval("${java.io.File::separator}"));
            Assert.StartsWith("java.security.AccessControlException", ex.Message);
        }

        [Fact]
        public void ClassAccess()
        {
            var ex = Assert.Throws<InterpretException>(() => Eval("${System::gc()}"));
            Assert.StartsWith("java.security.AccessControlException", ex.Message);
        }

        [Fact]
        public void ConstructorAccess()
        {
            var ex = Assert.Throws<InterpretException>(() => Eval("${new Date()}"));
            Assert.StartsWith("java.security.AccessControlException", ex.Message);
        }

        [Fact]
        public void MethodAccess()
        {
            var ex = Assert.Throws<InterpretException>(() => Eval("${'a'.length()}"));
            Assert.StartsWith("java.security.AccessControlException", ex.Message);
        }

        [Fact]
        public void FieldAccess()
        {
            var ex = Assert.Throws<InterpretException>(() => Eval("${Integer::MAX_VALUE}"));
            Assert.StartsWith("java.security.AccessControlException", ex.Message);
        }
    }
}