using System.Collections.Generic;
using Xunit;

namespace martin90s_ImagePicker.OriginalTests
{
    public interface IFileChooseInterceptor
    {
        bool OnFileChosen(object context, IList<string> sel, bool orig, int code, object action);
        int DescribeContents();
        void WriteToParcel(object dest, int flags);
    }

    public class FileChooseInterceptorTests
    {
        private class DummyImpl : IFileChooseInterceptor
        {
            public bool OnFileChosen(object context, IList<string> sel, bool orig, int code, object action)
            {
                return sel != null && sel.Count > 0 && orig && code == 2 && action == null;
            }

            public int DescribeContents() => 0;

            public void WriteToParcel(object dest, int flags) { }

            public static DummyImpl[] NewArray(int size) => new DummyImpl[size];
            public static DummyImpl CreateFromParcel(object source) => new DummyImpl();
        }

        [Fact]
        public void TestOnFileChosen()
        {
            var impl = new DummyImpl();
            var sel = new List<string> { "pic1" };
            Assert.True(impl.OnFileChosen(null, sel, true, 2, null));
        }

        [Fact]
        public void TestParcelable()
        {
            var impl = new DummyImpl();
            Assert.Equal(0, impl.DescribeContents());
            impl.WriteToParcel(null, 0); // no-op for coverage
            var arr = DummyImpl.NewArray(3);
            Assert.Equal(3, arr.Length);
            var inst = DummyImpl.CreateFromParcel(null);
            Assert.NotNull(inst);
        }
    }
}