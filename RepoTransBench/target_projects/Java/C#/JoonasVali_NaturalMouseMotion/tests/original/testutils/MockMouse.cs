using JoonasVali.NaturalMouseMotion.Api;

namespace JoonasVali.NaturalMouseMotion.Tests.Original.TestUtils
{
    public class MockMouse : MouseMotion
    {
        public override bool MoveTo(int x, int y)
        {
            return true;
        }
    }
}