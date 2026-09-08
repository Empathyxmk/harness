namespace Vasco.Tests.Original
{
    public class CallGraphTestCase
    {
        private class A
        {
            public void Foo() { Bar(); }
            public void Bar() { }
        }

        public static void Main(string[] args)
        {
            var a1 = new A();
            a1.Foo();

            var a2 = new A();
            a2.Foo();

            a2.Bar();
        }
    }
}