package de.flapdoodle.embed.process.store;

import de.flapdoodle.embed.process.config.store.IDownloadConfig;
import de.flapdoodle.embed.process.extract.ITempNaming;
import de.flapdoodle.embed.process.io.directories.IDirectory;
import org.junit.Test;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class NonCachedPostgresArtifactStoreBuilderTest {
    @Test
    public void builderShouldReturnPostgresArtifactStore() {
        NonCachedPostgresArtifactStoreBuilder builder = new NonCachedPostgresArtifactStoreBuilder();
        IDownloadConfig downloadConfig = mock(IDownloadConfig.class);
        IDirectory dir = mock(IDirectory.class);
        ITempNaming tempNaming = mock(ITempNaming.class);
        IDownloader downloader = mock(IDownloader.class);
        builder.downloadConfig(downloadConfig).tempDirFactory(dir).executableNaming(tempNaming).downloader(downloader);

        IArtifactStore store = builder.build();
        assertTrue(store instanceof PostgresArtifactStore);
    }
}