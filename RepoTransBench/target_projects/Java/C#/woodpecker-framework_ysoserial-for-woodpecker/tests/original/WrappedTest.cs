using System;
using System.Threading.Tasks;

namespace WoodpeckerYsoserial.Tests
{
    public interface IWrappedTest : ICustomPayloadArgs
    {
        Func<Task<object>> CreateCallable(Func<Task<object>> innerCallable);
    }
}