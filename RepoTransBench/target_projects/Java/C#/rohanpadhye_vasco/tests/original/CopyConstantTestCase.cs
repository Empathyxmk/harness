namespace Vasco.Tests.Original
{
    public class CopyConstantTestCase
    {
        public static void Main(string[] args)
        {
            var inner = new Inner(8);
            int x = inner.Sq();
            int y = inner.Val();
            int z = inner.Foo(8, 8);
            System.Console.WriteLine(x + y + z);
        }

        private class Inner
        {
            public int Data { get; set; }
            public Inner(int val)
            {
                Data = val;
            }
            public int Sq()
            {
                return Data * Data;
            }
            public int Val()
            {
                return Data;
            }
            public int Foo(int a, int b)
            {
                int x = a;
                int y = b;
                int z;
                if (a < 5)
                    z = x;
                else
                    z = y;
                return z;
            }
        }
    }
}