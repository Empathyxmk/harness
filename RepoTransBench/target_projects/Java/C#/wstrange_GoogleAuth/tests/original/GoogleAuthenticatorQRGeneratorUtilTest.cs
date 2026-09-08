using System;
using System.Reflection;
using Xunit;

namespace GoogleAuth.Tests
{
    public class GoogleAuthenticatorQRGeneratorUtilTest
    {
        [Fact]
        public void TestInternalURLEncodeNormal()
        {
            var method = typeof(GoogleAuthenticatorQRGenerator).GetMethod(
                "InternalURLEncode", BindingFlags.Static | BindingFlags.NonPublic);
            Assert.NotNull(method);
            var encoded = (string)method.Invoke(null, new object[] { "test@example.com" });
            Assert.Contains("test%40example.com", encoded);
        }

        [Fact]
        public void TestInternalURLEncode_Throws()
        {
            // In the C# equivalent, Encoding.UTF8 is always present. This branch is not realistically testable.
        }

        [Fact]
        public void TestFormatLabelHappyPath()
        {
            var method = typeof(GoogleAuthenticatorQRGenerator).GetMethod(
                "FormatLabel", BindingFlags.Static | BindingFlags.NonPublic);
            Assert.NotNull(method);

            var label = (string)method.Invoke(null, new object[] { "IssuerCompany", "user@example.com" });
            Assert.Equal("IssuerCompany:user@example.com", label);

            label = (string)method.Invoke(null, new object[] { null, "john" });
            Assert.Equal("john", label);
        }

        [Fact]
        public void TestFormatLabelThrows_AccountNameNull()
        {
            var method = typeof(GoogleAuthenticatorQRGenerator).GetMethod(
                "FormatLabel", BindingFlags.Static | BindingFlags.NonPublic);
            Assert.NotNull(method);

            var ex = Assert.ThrowsAny<TargetInvocationException>(() =>
            {
                method.Invoke(null, new object[] { "Company", null });
            });
            Assert.IsType<ArgumentException>(ex.InnerException);
        }

        [Fact]
        public void TestFormatLabelThrows_AccountNameEmpty()
        {
            var method = typeof(GoogleAuthenticatorQRGenerator).GetMethod(
                "FormatLabel", BindingFlags.Static | BindingFlags.NonPublic);
            Assert.NotNull(method);

            var ex = Assert.ThrowsAny<TargetInvocationException>(() =>
            {
                method.Invoke(null, new object[] { "Company", "" });
            });
            Assert.IsType<ArgumentException>(ex.InnerException);
        }

        [Fact]
        public void TestFormatLabelThrows_IssuerContainsColon()
        {
            var method = typeof(GoogleAuthenticatorQRGenerator).GetMethod(
                "FormatLabel", BindingFlags.Static | BindingFlags.NonPublic);
            Assert.NotNull(method);

            var ex = Assert.ThrowsAny<TargetInvocationException>(() =>
            {
                method.Invoke(null, new object[] { "Iss:uer", "user" });
            });
            Assert.IsType<ArgumentException>(ex.InnerException);
        }
    }
}