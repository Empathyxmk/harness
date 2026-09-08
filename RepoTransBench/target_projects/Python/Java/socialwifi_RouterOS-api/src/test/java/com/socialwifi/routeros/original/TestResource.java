package com.socialwifi.routeros.original;

import com.socialwifi.routeros.resource.Resource;
import com.socialwifi.routeros.api_communicator.ApiCommunicator;
import com.socialwifi.routeros.sentence.CommandSentence;
import com.socialwifi.routeros.sentence.ResponseSentence;
import com.socialwifi.routeros.query.Query;
import com.socialwifi.routeros.api_structure.ApiStructure;
import org.junit.jupiter.api.Test;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.List;
import java.util.Map;

class TestResource {

    @Test
    void testRunCommandWithResponse() {
        ApiCommunicator communicator = mock(ApiCommunicator.class);
        when(communicator.readResponse()).thenReturn(List.of(
                new ResponseSentence("re".getBytes(), Map.of("name".getBytes(), "abc".getBytes())),
                new ResponseSentence("done".getBytes(), Map.of())
        ));
        Resource resource = new Resource("/interface", communicator, mock(ApiStructure.class));
        List<Map<byte[], byte[]>> res = resource.runCommand(new CommandSentence("/interface".getBytes(), "print".getBytes()));
        assertEquals(1, res.size());
        assertArrayEquals("abc".getBytes(), res.get(0).get("name".getBytes()));
    }

    @Test
    void testRunCommandWithoutRe() {
        ApiCommunicator communicator = mock(ApiCommunicator.class);
        when(communicator.readResponse()).thenReturn(List.of(
                new ResponseSentence("done".getBytes(), Map.of())
        ));
        Resource resource = new Resource("/interface", communicator, mock(ApiStructure.class));
        List<Map<byte[], byte[]>> res = resource.runCommand(new CommandSentence("/interface".getBytes(), "print".getBytes()));
        assertTrue(res.isEmpty());
    }

    @Test
    void testCreatePrintCommand() {
        Resource resource = new Resource("/interface", mock(ApiCommunicator.class), mock(ApiStructure.class));
        CommandSentence command = resource.createPrint();
        assertArrayEquals("/interface/print".getBytes(), command.getApiFormat().get(0));
    }

    @Test
    void testCreatePrintQueryCommand() {
        Resource resource = new Resource("/interface", mock(ApiCommunicator.class), mock(ApiStructure.class));
        Query query = new Query().filter("name", "wlan0");
        CommandSentence command = resource.createPrint(query);
        assertEquals(2, command.getApiFormat().size());
        assertArrayEquals("/interface/print".getBytes(), command.getApiFormat().get(0));
        assertArrayEquals("?name=wlan0".getBytes(), command.getApiFormat().get(1));
    }

    @Test
    void testGetReturnData() {
        ApiCommunicator communicator = mock(ApiCommunicator.class);
        Resource resource = new Resource("/interface", communicator, mock(ApiStructure.class));
        CommandSentence command = resource.createPrint();
        assertEquals("/interface/print", new String(command.getApiFormat().get(0)));
    }
}