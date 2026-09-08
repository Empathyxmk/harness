package com.socialwifi.routeros.original;

import com.socialwifi.routeros.sentence.CommandSentence;
import com.socialwifi.routeros.sentence.ResponseSentence;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.List;
import java.util.Map;

class TestSentence {

    @Test
    void testCommandSentenceApiFormat() {
        CommandSentence sent = new CommandSentence("/interface".getBytes(), "set".getBytes());
        List<byte[]> apiFormat = sent.getApiFormat();
        assertArrayEquals("/interface".getBytes(), apiFormat.get(0));
        assertArrayEquals("set".getBytes(), apiFormat.get(1));
    }

    @Test
    void testResponseSentenceFieldLookup() {
        Map<byte[], byte[]> fields = Map.of("name".getBytes(), "eth0".getBytes());
        ResponseSentence resp = new ResponseSentence("re".getBytes(), fields);
        assertArrayEquals("eth0".getBytes(), resp.getField("name".getBytes()));
    }

    @Test
    void testResponseSentenceType() {
        ResponseSentence resp = new ResponseSentence("done".getBytes(), Map.of());
        assertArrayEquals("done".getBytes(), resp.type);
    }
}