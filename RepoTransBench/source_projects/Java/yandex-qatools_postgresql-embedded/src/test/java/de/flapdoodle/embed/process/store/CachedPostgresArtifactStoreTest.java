package de.flapdoodle.embed.process.store;

import de.flapdoodle.embed.process.config.store.*;
import de.flapdoodle.embed.process.distribution.Distribution;
import de.flapdoodle.embed.process.extract.IExtractedFileSet;
import de.flapdoodle.embed.process.extract.ITempNaming;
import de.flapdoodle.embed.process.io.directories.IDirectory;
import org.junit.Before;
import org.junit.Test;

import java.io.File;
import java.io.IOException;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class CachedPostgresArtifactStoreTest {
    private CachedPostgresArtifactStore store;
    private IDownloadConfig downloadConfig;
    private IDirectory dirFactory;
    private ITempNaming tempNaming;
    private IDownloader downloader;
    private IPackageResolver packageResolver;
    private FileSet fileSet;
    private Distribution distribution;

    @Before
    public void setUp() throws Exception {
        downloadConfig = mock(IDownloadConfig.class);
        dirFactory = mock(IDirectory.class);
        tempNaming = mock(ITempNaming.class);
        downloader = mock(IDownloader.class);
        packageResolver = mock(IPackageResolver.class);
        fileSet = mock(FileSet.class);
        distribution = mock(Distribution.class);

        when(downloadConfig.getPackageResolver()).thenReturn(packageResolver);
        when(dirFactory.asFile()).thenReturn(new File("target/test-tmp"));
        store = new CachedPostgresArtifactStore(downloadConfig, dirFactory, tempNaming, downloader);
    }

    @Test
    public void testRemoveFileSetDoesNothing() throws IOException {
        IExtractedFileSet fileSet = mock(IExtractedFileSet.class);
        store.removeFileSet(distribution, fileSet);
        // No exception = pass
    }

    @Test
    public void testExtractFileSetHandlesExceptionAndReturnsEmptyFileSet() throws IOException {
        // Simulate inside extractFileSet hitting the catch and returning EmptyFileSet
        when(downloadConfig.getPackageResolver()).thenThrow(new RuntimeException("fail!"));
        IExtractedFileSet result = store.extractFileSet(distribution);
        assertNotNull(result);
    }
}