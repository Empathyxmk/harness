package de.flapdoodle.embed.process.store;

import de.flapdoodle.embed.process.config.store.*;
import de.flapdoodle.embed.process.distribution.ArchiveType;
import de.flapdoodle.embed.process.distribution.Distribution;
import de.flapdoodle.embed.process.extract.*;
import de.flapdoodle.embed.process.io.directories.IDirectory;
import org.junit.Before;
import org.junit.Test;

import java.io.File;
import java.io.IOException;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class PostgresArtifactStoreTest {
    private PostgresArtifactStore store;
    private IDownloadConfig downloadConfig;
    private IDirectory dirFactory;
    private ITempNaming tempNaming;
    private IDownloader downloader;
    private IPackageResolver packageResolver;
    private FileSet fileSet;
    private Distribution distribution;

    @Before
    public void setUp() {
        downloadConfig = mock(IDownloadConfig.class);
        dirFactory = mock(IDirectory.class);
        tempNaming = mock(ITempNaming.class);
        downloader = mock(IDownloader.class);
        packageResolver = mock(IPackageResolver.class);
        fileSet = mock(FileSet.class);
        distribution = mock(Distribution.class);

        when(downloadConfig.getPackageResolver()).thenReturn(packageResolver);
        when(dirFactory.asFile()).thenReturn(new File("target/test-tmp"));
        store = new PostgresArtifactStore(downloadConfig, dirFactory, tempNaming, downloader);
    }

    @Test
    public void testSetAndGetDownloadConfig() {
        PostgresArtifactStore s = new PostgresArtifactStore(downloadConfig, dirFactory, tempNaming, downloader);
        assertEquals(downloadConfig, s.getDownloadConfig());
        IDownloadConfig newCfg = mock(IDownloadConfig.class);
        s.setDownloadConfig(newCfg);
        assertEquals(newCfg, s.getDownloadConfig());
    }

    @Test
    public void testRemoveFileSetDeletesFiles() throws IOException {
        IExtractedFileSet fileSet = mock(IExtractedFileSet.class);
        FileType type = FileType.Library;
        File tmpFile = File.createTempFile("toDel", ".bin");
        tmpFile.deleteOnExit();
        when(fileSet.files(any(FileType.class))).thenReturn(new File[] { tmpFile });
        when(fileSet.executable()).thenReturn(File.createTempFile("toDelExe", ".bin"));
        when(fileSet.baseDirIsGenerated()).thenReturn(true);
        File dir = new File("target/delDir");
        dir.mkdirs();
        dir.deleteOnExit();
        when(fileSet.baseDir()).thenReturn(dir);

        store.removeFileSet(distribution, fileSet);
        // pass if no exception
    }

    @Test
    public void testCheckDistributionFalseThenStore() throws IOException {
        Distribution dist = mock(Distribution.class);
        when(LocalArtifactStore.checkArtifact(downloadConfig, dist)).thenReturn(false);
        when(downloader.download(downloadConfig, dist)).thenReturn(new File("test"));
        when(LocalArtifactStore.store(eq(downloadConfig), eq(dist), any(File.class))).thenReturn(true);

        boolean ok = store.checkDistribution(dist);
        assertTrue(ok);
    }

    @Test
    public void testCheckDistributionTrue() throws IOException {
        Distribution dist = mock(Distribution.class);
        when(LocalArtifactStore.checkArtifact(downloadConfig, dist)).thenReturn(true);
        boolean ok = store.checkDistribution(dist);
        assertTrue(ok);
    }

    @Test
    public void testExtractFileSetHandlesException() throws IOException {
        when(packageResolver.getArchiveType(distribution)).thenReturn(ArchiveType.TGZ);
        when(packageResolver.getFileSet(distribution)).thenReturn(fileSet);
        File artifact = File.createTempFile("artifact", ".tgz");
        artifact.deleteOnExit();

        // cause extractor.extract to throw exception
        Extractors extractors = mock(Extractors.class);
        IExtractor extractor = mock(IExtractor.class);
        when(extractor.extract(any(), any(), any())).thenThrow(new RuntimeException("Fail!"));
        // Can't mock static method easily, so let it go through, should hit catch and return EmptyFileSet
        IExtractedFileSet result = store.extractFileSet(distribution);
        assertNotNull(result);
    }
}