namespace Feather.Tests.AndroidTest
{
    // Acts as a container for DI tests; no-op in .NET, present for parity with Java test structure.
    public class TestApplication
    {
        private object feather;

        public void OnCreate()
        {
            // .NET DI initialization would occur here with registered modules, if implemented.
            feather = new object();
        }

        public object Feather()
        {
            return feather;
        }
    }
}