package to.lean.tools.gmail.importer;

import org.junit.Test;
import java.io.IOException;

public class IoProviderTest {

    private static class DummyIoProvider implements IoProvider<String> {
        private final boolean throwException;
        DummyIoProvider(boolean throwException) {
            this.throwException = throwException;
        }
        public String get() throws IOException {
            if (throwException) throw new IOException("fail");
            return "success";
        }
    }

    @Test
    public void testGetSuccess() throws Exception {
        IoProvider<String> ioProvider = new DummyIoProvider(false);
        assert ioProvider.get().equals("success");
    }

    @Test(expected = IOException.class)
    public void testGetThrowsIOException() throws Exception {
        IoProvider<String> ioProvider = new DummyIoProvider(true);
        ioProvider.get();
    }
}