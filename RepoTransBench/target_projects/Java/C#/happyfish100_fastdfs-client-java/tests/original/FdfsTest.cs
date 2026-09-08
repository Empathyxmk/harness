using System;
using System.IO;
using Xunit;
using FastDFSClient;
using System.Linq;

namespace FastDFSClient.Tests
{
    public class FdfsTest : IDisposable
    {
        private StorageClient storageClient;
        private TrackerServer trackerServer;
        private const string CONF_NAME = "fdfstest.conf";
        private readonly string testLogDir = "./tmp_test_fdfs/";

        public FdfsTest()
        {
            // Setup test environment before each test
            Directory.CreateDirectory(testLogDir);
            ClientGlobal.Init(CONF_NAME);
            TrackerClient tracker = new TrackerClient();
            trackerServer = tracker.GetTrackerServer();
            StorageServer storageServer = null;
            storageClient = new StorageClient(trackerServer, storageServer);
        }

        public void Dispose()
        {
            storageClient?.Close();
        }

        private void WriteByteToFile(byte[] fbyte, string fileName)
        {
            string outPath = Path.Combine(testLogDir, fileName);
            System.IO.File.WriteAllBytes(outPath, fbyte);
        }

        [Fact]
        public void Upload()
        {
            NameValuePair[] metaList = new NameValuePair[1];
            string local_filename = "build.PNG";
            metaList[0] = new NameValuePair("fileName", local_filename);
            string filePath = Path.Combine(testLogDir, "build.PNG");
            byte[] bytes = new byte[16];
            for (int i = 0; i < 16; i++) bytes[i] = (byte)(i + 1);
            File.WriteAllBytes(filePath, bytes);

            byte[] inbytes = File.ReadAllBytes(filePath);
            string[] result = storageClient.UploadFile(inbytes, null, metaList);
            Assert.Equal(2, result.Length);
        }

        [Fact]
        public void Download()
        {
            string[] uploadresult = { "group1", "M00/00/00/J2fL12PVypeAWiGcAAM_gDeWVyw5817085" };
            byte[] result = storageClient.DownloadFile(uploadresult[0], uploadresult[1]);
            string local_filename = "commitment.d2f57e10.jpg";
            WriteByteToFile(result, local_filename);
            string filePath = Path.Combine(testLogDir, local_filename);
            Assert.True(File.Exists(filePath));
        }

        [Fact]
        public void TestUploadDownload()
        {
            NameValuePair[] metaList = new NameValuePair[1];
            string local_filename = "commitment.d2f57e10 (2).jpg";
            metaList[0] = new NameValuePair("fileName", local_filename);
            string filePath = Path.Combine(testLogDir, "commitment.d2f57e10 (2).jpg");
            byte[] bytes = new byte[32];
            for (int i = 0; i < 32; i++) bytes[i] = (byte)(i + 2);
            File.WriteAllBytes(filePath, bytes);

            byte[] inbytes = File.ReadAllBytes(filePath);
            string[] result = storageClient.UploadFile(inbytes, null, metaList);

            byte[] resultbytes = storageClient.DownloadFile(result[0], result[1]);
            WriteByteToFile(resultbytes, local_filename);
            string downFile = Path.Combine(testLogDir, local_filename);
            Assert.True(File.Exists(downFile));
        }
    }
}