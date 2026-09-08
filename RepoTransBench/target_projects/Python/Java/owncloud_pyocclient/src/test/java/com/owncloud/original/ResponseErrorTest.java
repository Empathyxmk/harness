package com.owncloud.original;

import static org.junit.jupiter.api.Assertions.*;

import java.time.LocalDate;
import java.time.ZoneOffset;
import java.util.Date;
import java.util.HashMap;
import java.time.Instant;
import java.util.Map;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;

class ResponseErrorTest {

    private static class FakeRes {
        public int status_code;
        public Object content;

        public FakeRes(int status_code, Object content) {
            this.status_code = status_code;
            this.content = content;
        }

        public FakeRes(int status_code) { // For test_repr_and_branching
            this.status_code = status_code;
        }
    }

    // Placeholder: Replace with your implementation of ResponseError and related utilities
    static class ResponseError extends RuntimeException {
        public int status_code;
        private Object body;
        private String message;
        public ResponseError(int status_code, String msg) {
            super(msg + " error: " + status_code);
            this.status_code = status_code;
            this.message = msg + " error: " + status_code;
        }
        public ResponseError(FakeRes res, String msg) {
            super("HTTP error: " + res.status_code + " (" + msg + ")");
            this.status_code = res.status_code;
            this.body = res.content;
        }
        public ResponseError(int status_code) {
            super("HTTP error: " + status_code);
            this.status_code = status_code;
        }
        public ResponseError(FakeRes res) {
            super("HTTP error: " + res.status_code);
            this.status_code = res.status_code;
            this.body = res.content;
        }
        public Object get_resource_body() {
            return body;
        }

        @Override
        public String toString() {
            return this.getMessage();
        }
    }

    static class OCSResponseError extends ResponseError {
        public OCSResponseError(FakeRes res) {
            super(res);
        }

        @Override
        public String toString() {
            if (get_resource_body() != null && get_resource_body() instanceof byte[]) {
                String xml = new String((byte[]) get_resource_body());
                if (xml.contains("<message>") && xml.contains("</message>")) {
                    String msg = xml.substring(xml.indexOf("<message>") + 9, xml.indexOf("</message>"));
                    return "OCS response error: " + msg;
                }
            }
            return "OCS response error: " + get_resource_body();
        }
    }

    @Test
    void test_init_with_int() {
        ResponseError err = new ResponseError(404, "MyErr");
        assertEquals(404, err.status_code);
        assertEquals("MyErr error: 404", err.toString());
    }

    @Test
    void test_init_with_response() {
        FakeRes res = new FakeRes(400, "resbody".getBytes());
        ResponseError err = new ResponseError(res, "OCS");
        assertEquals(400, err.status_code);
        assertArrayEquals("resbody".getBytes(), (byte[]) err.get_resource_body());
        assertTrue(err.toString().startsWith("HTTP error: 400 (OCS)"));
    }

    @Test
    void test_init_with_response_strcontent() {
        FakeRes res = new FakeRes(501, "Some string");
        ResponseError err = new ResponseError(res, "Txt");
        assertEquals(501, err.status_code);
        assertEquals("Some string", err.get_resource_body());
        assertTrue(err.toString().contains("Some string"));
    }

    @Test
    void test_repr_and_branching() {
        ResponseError rr = new ResponseError(401);
        assertEquals("HTTP error: 401", rr.toString());
        // test with no content property in response
        FakeRes res = new FakeRes(500);
        ResponseError err2 = new ResponseError(res);
        assertNull(err2.get_resource_body());
        assertTrue(err2.toString().contains("HTTP error: 500"));
    }

    @Test
    void test_ocs_xml_msg() {
        FakeRes res = new FakeRes(500, "<root><message>failmsg</message></root>".getBytes());
        OCSResponseError err = new OCSResponseError(res);
        assertTrue(err.toString().contains("failmsg"));
        assertArrayEquals("<root><message>failmsg</message></root>".getBytes(), (byte[]) err.get_resource_body());
    }

    @Test
    void test_ocs_xml_invalid() {
        FakeRes res = new FakeRes(400, "not<xml".getBytes());
        OCSResponseError err = new OCSResponseError(res);
        assertTrue(err.toString().contains("OCS response error"));
        assertArrayEquals("not<xml".getBytes(), (byte[]) err.get_resource_body());
    }

    @Test
    void test_ocs_none() {
        FakeRes res = new FakeRes(0, null);
        res.status_code = 0;
        OCSResponseError err = new OCSResponseError(res);
        assertNull(err.get_resource_body());
    }
}