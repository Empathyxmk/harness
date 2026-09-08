package to.lean.tools.gmail.importer;

import org.junit.Before;
import org.junit.Test;
import org.mockito.ArgumentCaptor;
import org.mockito.Mockito;
import to.lean.tools.gmail.importer.gmail.GmailSyncer;
import to.lean.tools.gmail.importer.local.LocalMessage;
import to.lean.tools.gmail.importer.local.LocalStorage;

import java.io.IOException;
import java.util.Arrays;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.logging.Logger;
import javax.mail.MessagingException;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class ImporterTest {

    private Logger logger;
    private MailProvider<LocalStorage> storageProvider;
    private GmailSyncer gmailSyncer;
    private CommandLineArguments args;
    private Importer importer;

    @Before
    @SuppressWarnings("unchecked")
    public void setUp() throws Exception {
        logger = Logger.getAnonymousLogger();
        storageProvider = mock(MailProvider.class);
        gmailSyncer = mock(GmailSyncer.class);
        args = new CommandLineArguments();
        importer = new Importer(logger, storageProvider, gmailSyncer, args);
    }

    @Test
    public void testImportsNoMessages() throws Exception {
        LocalStorage storage = mock(LocalStorage.class);
        when(storage.iterator()).thenReturn(Collections.<LocalMessage>emptyList().iterator());
        when(storageProvider.get()).thenReturn(storage);

        importer.importMail();

        verify(gmailSyncer).init();
        verify(gmailSyncer, never()).sync(anyList());
    }

    @Test
    public void testImportsSomeMessagesWithMaxMessages() throws Exception {
        LocalMessage msg1 = mock(LocalMessage.class);
        when(msg1.getMessageId()).thenReturn("1");
        when(msg1.getFolders()).thenReturn(Arrays.asList("INBOX"));
        LocalMessage msg2 = mock(LocalMessage.class);
        when(msg2.getMessageId()).thenReturn("2");
        when(msg2.getFolders()).thenReturn(Arrays.asList("INBOX"));

        Iterator<LocalMessage> iterator = Arrays.asList(msg1, msg2).iterator();
        LocalStorage storage = mock(LocalStorage.class);
        when(storage.iterator()).thenReturn(iterator);
        when(storageProvider.get()).thenReturn(storage);

        args.maxMessages = 1;

        importer.importMail();

        verify(gmailSyncer).init();
        ArgumentCaptor<List> captor = ArgumentCaptor.forClass(List.class);
        verify(gmailSyncer).sync(captor.capture());
        assertEquals(1, captor.getValue().size());
        assertEquals(msg1, captor.getValue().get(0));
    }

    @Test
    public void testBatchingBehavior() throws Exception {
        // Create more than BATCH_SIZE messages to test batching (BATCH_SIZE = 100)
        int batchSize = 100;
        int totalMessages = batchSize + 10;
        LocalMessage[] messages = new LocalMessage[totalMessages];
        for (int i = 0; i < totalMessages; i++) {
            LocalMessage msg = mock(LocalMessage.class);
            when(msg.getMessageId()).thenReturn(String.valueOf(i));
            when(msg.getFolders()).thenReturn(Arrays.asList("INBOX"));
            messages[i] = msg;
        }
        LocalStorage storage = mock(LocalStorage.class);
        when(storage.iterator()).thenReturn(Arrays.asList(messages).iterator());
        when(storageProvider.get()).thenReturn(storage);

        args.maxMessages = null;

        importer.importMail();

        verify(gmailSyncer).init();
        verify(gmailSyncer, times(2)).sync(anyList());
    }

    @Test(expected = MessagingException.class)
    public void testStorageProviderThrowsMessagingException() throws Exception {
        when(storageProvider.get()).thenThrow(new MessagingException("fail"));
        importer.importMail();
    }

    @Test(expected = IOException.class)
    public void testGmailSyncerThrowsIOException() throws Exception {
        LocalStorage storage = mock(LocalStorage.class);
        when(storage.iterator()).thenReturn(Collections.<LocalMessage>emptyList().iterator());
        when(storageProvider.get()).thenReturn(storage);

        doThrow(new IOException("fail")).when(gmailSyncer).init();

        importer.importMail();
    }
}