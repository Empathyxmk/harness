package to.lean.tools.gmail.importer;

import org.junit.Test;
import javax.mail.MessagingException;

public class MailProviderTest {

    private static class DummyMailProvider implements MailProvider<String> {
        private final boolean throwException;
        DummyMailProvider(boolean throwException) {
            this.throwException = throwException;
        }
        public String get() throws MessagingException {
            if (throwException) throw new MessagingException("fail");
            return "success";
        }
    }

    @Test
    public void testGetSuccess() throws Exception {
        MailProvider<String> mailProvider = new DummyMailProvider(false);
        assert mailProvider.get().equals("success");
    }

    @Test(expected = MessagingException.class)
    public void testGetThrowsMessagingException() throws Exception {
        MailProvider<String> mailProvider = new DummyMailProvider(true);
        mailProvider.get();
    }
}