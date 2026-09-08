using System;
using System.Collections.Generic;
using System.IO;
using Xunit;

namespace martin90s_ImagePicker.PublicTests
{
    public class CapturePhotoHelperPublicTests
    {
        public class DummyActivity
        {
            public object? LastIntent = null;
            public int LastRequestCode = -1;
            public DummyPackageManager PkgMgr;
            public DummyActivity(DummyPackageManager pm) { PkgMgr = pm; }
            public void StartActivityForResult(object intent, int requestCode)
            {
                LastIntent = intent;
                LastRequestCode = requestCode;
            }
            public DummyPackageManager GetPackageManager() => PkgMgr;
            public DummyActivity GetApplicationContext() => this;
        }

        public class DummyFragment
        {
            public object? LastIntent;
            public int LastRequestCode;
            private DummyActivity Activity;
            public DummyFragment(DummyActivity act) { Activity = act; }
            public void StartActivityForResult(object intent, int requestCode)
            {
                LastIntent = intent;
                LastRequestCode = requestCode;
            }
            public DummyActivity GetActivity() => Activity;
            public DummyActivity GetContext() => Activity;
        }

        public class DummyPackageManager
        {
            public List<string> Acts;
            public DummyPackageManager(List<string> l) { Acts = l; }
            public List<string> QueryIntentActivities(object intent, int flags) => Acts;
        }

        private DummyPackageManager withCamera;
        private DummyPackageManager withoutCamera;
        private DummyActivity dummyAct;
        private DummyFragment dummyFrag;

        public CapturePhotoHelperPublicTests()
        {
            withCamera = new DummyPackageManager(new List<string> { "camera1", "camera2" }); // 2 cameras
            withoutCamera = new DummyPackageManager(new List<string>());
            dummyAct = new DummyActivity(withCamera);
            dummyFrag = new DummyFragment(dummyAct);
        }

        [Fact]
        public void TestHasCameraTrueAndFalse_Public()
        {
            var hpAct = new CapturePhotoHelperStub(dummyAct);
            Assert.True(hpAct.HasCamera());
            var noCamAct = new DummyActivity(withoutCamera);
            var hpNoCam = new CapturePhotoHelperStub(noCamAct);
            Assert.False(hpNoCam.HasCamera());
        }

        [Fact]
        public void TestSetPhotoAndGetPhoto_Public()
        {
            var hp = new CapturePhotoHelperStub(dummyAct);
            string filePath = Path.Combine(Path.GetTempPath(), Guid.NewGuid().ToString() + "_unique_img.png");
            hp.SetPhoto(filePath);
            var file = hp.GetPhoto();
            Assert.Equal(filePath, file);
        }

        [Fact]
        public void TestCreatePhotoFileFallback_Public()
        {
            var hp = new CapturePhotoHelperStub(dummyAct);
            hp.PhotoFolder = null;
            hp.CreatePhotoFile();
            Assert.Null(hp.GetPhoto());
        }

        [Fact]
        public void TestCapturePhoto_WithUri_Public()
        {
            var hpFrag = new CapturePhotoHelperStub(dummyFrag);
            var uri = "content://different/path";
            hpFrag.CapturePhoto(uri);
            Assert.NotNull(dummyFrag.LastIntent);
            Assert.Equal(CapturePhotoHelperStub.CAPTURE_PHOTO_REQUEST_CODE, dummyFrag.LastRequestCode);

            var hpAct = new CapturePhotoHelperStub(dummyAct);
            dummyAct.LastIntent = null;
            hpAct.CapturePhoto(uri);
            Assert.NotNull(dummyAct.LastIntent);
            Assert.Equal(CapturePhotoHelperStub.CAPTURE_PHOTO_REQUEST_CODE, dummyAct.LastRequestCode);
        }

        [Fact]
        public void TestCapturePhoto_NullUri_Public()
        {
            var hp = new CapturePhotoHelperStub(dummyAct);
            hp.CapturePhoto(null);
            Assert.Null(dummyAct.LastIntent);
        }

        // Decoupled stub as in original
        public class CapturePhotoHelperStub
        {
            public const int CAPTURE_PHOTO_REQUEST_CODE = 1000;
            private object _host;
            public string? PhotoFile;
            public string? PhotoFolder = Path.GetTempPath();
            public CapturePhotoHelperStub(object host)
            {
                _host = host;
            }
            public bool HasCamera()
            {
                var mgr = _host is DummyActivity a ? a.GetPackageManager() : null;
                if (mgr == null) return false;
                var l = mgr.QueryIntentActivities(null, 0);
                return l != null && l.Count > 0;
            }
            public void SetPhoto(string path)
            {
                PhotoFile = path;
            }
            public string? GetPhoto()
            {
                return PhotoFile;
            }
            public void CreatePhotoFile()
            {
                if (PhotoFolder == null)
                {
                    PhotoFile = null;
                }
                else
                {
                    PhotoFile = Path.Combine(PhotoFolder, Guid.NewGuid().ToString("N") + ".jpg");
                }
            }
            public void CapturePhoto(string? uri)
            {
                if (uri == null) return;
                if (_host is DummyFragment frag)
                    frag.StartActivityForResult(new object(), CAPTURE_PHOTO_REQUEST_CODE);
                else if (_host is DummyActivity act)
                    act.StartActivityForResult(new object(), CAPTURE_PHOTO_REQUEST_CODE);
            }
        }
    }
}