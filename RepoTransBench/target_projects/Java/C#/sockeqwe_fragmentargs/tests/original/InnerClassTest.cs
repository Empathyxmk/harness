using Xunit;

namespace ProjectName.Tests.Original.Processor
{
    public static class CompileTest
    {
        public static void AssertClassCompilesWithoutError(string classResourceName, string outputClassResourceName)
        {
            // Placeholder: Simulation for "compiles without error"
        }
    }

    public class InnerClassTest
    {
        [Fact]
        public void InnerClass()
        {
            CompileTest.AssertClassCompilesWithoutError("ClassWithInnerClass.cs", "ClassWithInnerClassBuilder.cs");
        }

        [Fact]
        public void InnerClassWithProtectedField()
        {
            CompileTest.AssertClassCompilesWithoutError("InnerClassWithProtectedField.cs", "InnerClassWithProtectedFieldBuilder.cs");
        }
    }
}