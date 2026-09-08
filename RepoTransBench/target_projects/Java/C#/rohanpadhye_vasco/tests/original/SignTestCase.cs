namespace Vasco.Tests.Original
{
    public class SignTestCase
    {
        public static int P, Q, R;

        public static void Main(string[] args)
        {
            int p = Five();
            int q = F(p, -3);
            int r = G(-q);
            P = p;
            Q = q;
            R = r;
        }

        public static int Five()
        {
            return 5;
        }

        public static int F(int a, int b)
        {
            int c;
            if (a < b)
            {
                c = a * b;
            }
            else
            {
                c = G(10);
            }
            return c;
        }

        public static int G(int u)
        {
            int v = F(-u, u);
            return v;
        }
    }
}