using System;
using System.Collections.Generic;
using Xunit;

namespace martin90s_ImagePicker.PublicTests
{
    public class PickerConfig
    {
        public virtual object GetAppContext() => null;
    }
    public class PickerAction { }
    public class SImagePicker
    {
        public static readonly int MODE_IMAGE = 2;
        public static PickerConfig? pickerConfig;
        public static void Init(PickerConfig config) => pickerConfig = config;
        public static PickerConfig GetPickerConfig()
            => pickerConfig ?? throw new ArgumentException();
        public static SImagePicker From(object input)
        {
            if (pickerConfig == null) throw new ArgumentException();
            return new SImagePicker(input);
        }
        private object _input;
        public SImagePicker(object input) { _input = input; }
        public SImagePicker MaxCount(int x) { return this; }
        public SImagePicker RowCount(int x) { return this; }
        public SImagePicker PickMode(int x) { return this; }
        public SImagePicker CropFilePath(string path) { return this; }
        public SImagePicker ShowCamera(bool show) { return this; }
        public SImagePicker PickText(int x) { return this; }
        public SImagePicker SetSelected(List<string> sel) { return this; }
        public SImagePicker FileInterceptor(object? inter) { return this; }
        public void ForResult(int requestCode)
        {
            if (_input == null) throw new ArgumentException();
        }
    }
    public class DummyActivity
    {
        public object? LastIntent;
        public int LastRequestCode;
    }
    public class DummyFragment
    {
        private DummyActivity _act;
        public object? LastIntent;
        public int LastRequestCode;
        public DummyFragment(DummyActivity act) { _act = act; }
        public DummyActivity GetActivity() => _act;
        public object? GetContext() => _act;
        public void StartActivityForResult(object intent, int requestCode)
        {
            LastIntent = intent;
            LastRequestCode = requestCode;
        }
    }

    public class SImagePickerPublicTests
    {
        private class DummyConfig : PickerConfig
        {
            private object _ctx;
            public DummyConfig(object ctx) { _ctx = ctx; }
            public override object GetAppContext() => _ctx;
        }

        private DummyActivity dummyActivity;
        private DummyFragment dummyFragment;

        public SImagePickerPublicTests()
        {
            dummyActivity = new DummyActivity();
            dummyFragment = new DummyFragment(dummyActivity);
            SImagePicker.Init(new DummyConfig(dummyActivity));
        }

        [Fact]
        public void TestGetPickerConfig_ExceptionIfNotInitialized_Public()
        {
            SImagePicker.Init(new DummyConfig(dummyActivity));
            SImagePicker.pickerConfig = null;
            Assert.Throws<ArgumentException>(() => SImagePicker.GetPickerConfig());
        }

        [Fact]
        public void TestForResult_NoInit_Throws_Public()
        {
            SImagePicker.pickerConfig = null;
            Assert.Throws<ArgumentException>(() => SImagePicker.From(dummyActivity).ForResult(11));
        }

        [Fact]
        public void TestFromActivityAndFromFragment_Public()
        {
            var picker1 = SImagePicker.From(dummyActivity);
            Assert.NotNull(picker1);
            var picker2 = SImagePicker.From(dummyFragment);
            Assert.NotNull(picker2);
        }

        [Fact]
        public void TestMaxCountRowCountPickModeCropFileShowCameraPickTextSetSelected_Public()
        {
            var picker = SImagePicker.From(dummyActivity);
            var selected = new List<string> { "abc" };
            var result = picker.MaxCount(3).RowCount(5).PickMode(SImagePicker.MODE_IMAGE)
                .CropFilePath("other_file.png").ShowCamera(false).PickText(456).SetSelected(selected);
            Assert.NotNull(result);
        }

        [Fact]
        public void TestForResultCallsActivityAndFragment_Public()
        {
            var pickerA = SImagePicker.From(dummyActivity);
            pickerA.ForResult(42);
            Assert.NotNull(dummyActivity.LastIntent);
            Assert.Equal(42, dummyActivity.LastRequestCode);

            var pickerF = SImagePicker.From(dummyFragment);
            pickerF.ForResult(24);
            Assert.NotNull(dummyFragment.LastIntent);
            Assert.Equal(24, dummyFragment.LastRequestCode);
        }

        [Fact]
        public void TestForResult_NeitherActivityNorFragment_Public()
        {
            var picker = new SImagePicker(null);
            SImagePicker.pickerConfig = new DummyConfig(dummyActivity);
            Assert.Throws<ArgumentException>(() => picker.ForResult(999));
        }

        [Fact]
        public void TestFileInterceptor_Public()
        {
            var picker = SImagePicker.From(dummyActivity);
            object inter = new object();
            var res = picker.FileInterceptor(inter);
            Assert.NotNull(res);
        }
    }
}