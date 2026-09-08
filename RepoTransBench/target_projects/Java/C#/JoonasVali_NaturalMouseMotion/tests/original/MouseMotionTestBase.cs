using Xunit;
using JoonasVali.NaturalMouseMotion.Api;

namespace JoonasVali.NaturalMouseMotion.Tests.Original
{
    public abstract class MouseMotionTestBase
    {
        protected MouseMotion GetMouseMotion()
        {
            return new MouseMotion();
        }
    }
}