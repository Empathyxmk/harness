package to.lean.tools.gmail.importer;

import org.junit.Test;
import javax.mail.MessagingException;

public class MailProviderPublicTest {

    private static class AnotherDummyMailProvider implements MailProvider<Integer> {
        private final boolean shouldThrow;
        AnotherDummyMailProvider(boolean shouldThrow) {
            this.shouldThrow = shouldThrow;
        }
        public Integer get() throws MessagingException {
            if (shouldThrow) throw new MessagingException("provider fail");
            return 12345;
        }
    }

    @Test
    public void testGetDifferentSuccess() throws Exception {
        MailProvider<Integer> mailProvider = new AnotherDummyMailProvider(false);
        assert mailProvider.get().equals(12345);
    }

    @Test(expected = MessagingException.class)
    public void testGetThrowsMessagingExceptionPublic() throws Exception {
        MailProvider<Integer> mailProvider = new AnotherDummyMailProvider(true);
        mailProvider.get();
    }
}