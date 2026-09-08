package to.lean.tools.gmail.importer.gmail;

import com.google.api.client.http.HttpResponse;
import com.google.api.client.http.HttpResponseInterceptor;
import org.junit.Test;

import java.io.IOException;

import static org.mockito.Mockito.*;

public class UnsuccessfulResponseHandlerChainerPublicTest {

    @Test
    public void testDifferentInterceptorChainDelegates() throws IOException {
        HttpResponseInterceptor interceptor1 = mock(HttpResponseInterceptor.class);
        HttpResponseInterceptor interceptor2 = mock(HttpResponseInterceptor.class);
        HttpResponse response = mock(HttpResponse.class);
        UnsuccessfulResponseHandlerChainer chain = new UnsuccessfulResponseHandlerChainer(interceptor1, interceptor2);

        chain.interceptResponse(response);

        verify(interceptor1).interceptResponse(response);
        verify(interceptor2).interceptResponse(response);
    }
}