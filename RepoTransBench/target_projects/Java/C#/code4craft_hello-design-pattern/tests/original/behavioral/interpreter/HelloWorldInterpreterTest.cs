using Xunit;

namespace HelloDesignPattern.Tests.behavioral.interpreter
{
    public class HelloWorldInterpreterTest
    {
        [Fact]
        public void TestInterpret()
        {
            var input = "Hello Interpreter!";
            var interpreter = new HelloWorldInterpreter();
            interpreter.Interpret(input);
        }
    }
}