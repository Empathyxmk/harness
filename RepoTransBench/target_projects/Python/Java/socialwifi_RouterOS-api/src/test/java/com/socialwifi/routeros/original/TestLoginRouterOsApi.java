package com.socialwifi.routeros.original;

import com.socialwifi.routeros.base_api.Connection;
import com.socialwifi.routeros.login_router_os_api.LoginRouterOsApi;
import com.socialwifi.routeros.exceptions.AuthenticationFailed;
import com.socialwifi.routeros.api_communicator.ApiCommunicator;
import com.socialwifi.routeros.sentence.ResponseSentence;
import org.junit.jupiter.api.Test;
import java.util.List;
import java.util.Map;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

class TestLoginRouterOsApi {

    @Test
    void testLoginSuccess() {
        Connection connection = mock(Connection.class);
        ApiCommunicator communicator = mock(ApiCommunicator.class);
        ResponseSentence re = new ResponseSentence("done".getBytes(), Map.of());
        when(communicator.readResponse()).thenReturn(List.of(re));

        LoginRouterOsApi api = new LoginRouterOsApi(communicator, connection);
        assertDoesNotThrow(() -> api.login("admin", "correctpassword"));
    }

    @Test
    void testLoginFailed() {
        Connection connection = mock(Connection.class);
        ApiCommunicator communicator = mock(ApiCommunicator.class);
        ResponseSentence trap = new ResponseSentence("trap".getBytes(), Map.of("message".getBytes(), "invalid credentials".getBytes()));
        when(communicator.readResponse()).thenReturn(List.of(trap));

        LoginRouterOsApi api = new LoginRouterOsApi(communicator, connection);
        assertThrows(AuthenticationFailed.class, () -> api.login("admin", "wrongpassword"));
    }
}