package com.socialwifi.routeros.original;

import com.socialwifi.routeros.api_communicator.ApiCommunicator;
import com.socialwifi.routeros.base_api.Connection;
import com.socialwifi.routeros.sentence.CommandSentence;
import com.socialwifi.routeros.sentence.ResponseSentence;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class TestApiCommunicator {

    @Test
    void testSendApiCommandsCallsConnection() {
        Connection connection = mock(Connection.class);
        ApiCommunicator communicator = new ApiCommunicator(connection);

        CommandSentence commandSentence = mock(CommandSentence.class);
        when(commandSentence.getApiFormat()).thenReturn(List.of("foo".getBytes(), "bar".getBytes()));
        communicator.sendApiCommand(commandSentence);

        ArgumentCaptor<List<byte[]>> captor = ArgumentCaptor.forClass(List.class);
        verify(connection, times(1)).sendSentence(captor.capture());

        List<byte[]> sentList = captor.getValue();
        assertEquals(2, sentList.size());
        assertArrayEquals("foo".getBytes(), sentList.get(0));
        assertArrayEquals("bar".getBytes(), sentList.get(1));
    }

    @Test
    void testReadResponseSingleSentence() {
        Connection connection = mock(Connection.class);
        ApiCommunicator communicator = new ApiCommunicator(connection);

        when(connection.receiveSentence()).thenReturn(
                List.of("!done".getBytes())
        );
        List<ResponseSentence> responses = communicator.readResponse();
        assertEquals(1, responses.size());
        assertArrayEquals("done".getBytes(), responses.get(0).type);
    }

    @Test
    void testReadResponseMultipleSentences() {
        Connection connection = mock(Connection.class);
        ApiCommunicator communicator = new ApiCommunicator(connection);

        when(connection.receiveSentence())
                .thenReturn(List.of("!re".getBytes()))
                .thenReturn(List.of("!done".getBytes()));

        List<ResponseSentence> responses = communicator.readResponse();
        assertEquals(2, responses.size());
        assertArrayEquals("re".getBytes(), responses.get(0).type);
        assertArrayEquals("done".getBytes(), responses.get(1).type);
    }
}