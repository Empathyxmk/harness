package com.example.jsonrpc.original;

import com.example.jsonrpc.exceptions.JSONRPCError;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class TestJsonrpcErrors {

    @Test
    void testJsonrpcParseError() {
        JSONRPCError err = JSONRPCError.PARSE_ERROR;
        assertEquals(-32700, err.getCode());
        assertEquals("Parse error", err.getMessage());
    }

    @Test
    void testJsonrpcInvalidRequest() {
        JSONRPCError err = JSONRPCError.INVALID_REQUEST;
        assertEquals(-32600, err.getCode());
        assertEquals("Invalid Request", err.getMessage());
    }
}