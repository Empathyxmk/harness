package to.lean.tools.gmail.importer.gmail;

import org.junit.Test;

import java.util.Collections;

import static org.mockito.Mockito.*;

public class GmailSyncerPublicTest {

    @Test
    public void testDifferentInitTriggersSyncPublic() throws Exception {
        GmailSyncer syncer = mock(GmailSyncer.class);
        syncer.init();
        verify(syncer).init();
        syncer.sync(Collections.emptyList());
        verify(syncer).sync(Collections.emptyList());
    }
}