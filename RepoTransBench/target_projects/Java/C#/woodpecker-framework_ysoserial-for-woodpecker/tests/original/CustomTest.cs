using System;
using System.Threading.Tasks;

namespace WoodpeckerYsoserial.Tests
{
    public interface ICustomTest : ICustomPayloadArgs
    {
        void Run(Func<Task<object>> payload);
    }
}