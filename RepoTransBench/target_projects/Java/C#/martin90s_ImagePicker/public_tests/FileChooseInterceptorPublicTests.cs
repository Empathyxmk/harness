using System.Collections.Generic;
using Xunit;

namespace martin90s_ImagePicker.PublicTests
{
    public interface IFileChooseInterceptor
    {
        bool OnFileChosen(object context, IList<string> sel, bool orig, int code, object action);
        int DescribeContents();
        void WriteToParcel(object dest, int flags);
    }

    public class FileChooseInterceptorPublicTests
    {
        private class DummyImpl : IFileChooseInterceptor
        {
            public bool OnFileChosen(object context, IList<string> sel, bool orig, int code, object action)
            {
                // Different data: sel.Count > 1, !orig, code==5, action!=null
                return sel != null && sel.Count > 1 && !orig && code == 5 && action != null;
            }
            public int DescribeContents() => 0;
            public void WriteToParcel(object dest, int flags) { }
            public static DummyImpl[] NewArray(int size) => new DummyImpl[size];
            public static DummyImpl CreateFromParcel(object source) => new DummyImpl();
        }

        [Fact]
        public void TestOnFileChosenWithDifferentData()
        {
            var impl = new DummyImpl();
            var sel = new List<string>() { "picA", "picB" };
            Assert.True(impl.OnFileChosen(null, sel, false, 5, new object()));
        }

        [Fact]
        public void TestParcelableDifferentSize()
        {
            var impl = new DummyImpl();
            Assert.Equal(0, impl.DescribeContents());
            impl.WriteToParcel(null, 0);
            var arr = DummyImpl.NewArray(2);
            Assert.Equal(2, arr.Length);
            var inst = DummyImpl.CreateFromParcel(null);
            Assert.NotNull(inst);
        }
    }
}