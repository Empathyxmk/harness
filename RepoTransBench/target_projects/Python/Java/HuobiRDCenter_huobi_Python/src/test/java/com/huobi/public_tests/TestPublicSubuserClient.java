package com.huobi.public_tests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

public class TestPublicSubuserClient {

    static class DummySubuserClientPublic {
        String apiKey = null;
        String secretKey = null;

        DummySubuserClientPublic() {}
        DummySubuserClientPublic(String apiKey, String secretKey) {
            this.apiKey = apiKey;
            this.secretKey = secretKey;
        }

        public List<Map<String, Object>> postSetSubuserTransferability(String subUids, Object transferability) {
            if (subUids == null) throw new IllegalArgumentException("sub_uids required");
            if (transferability instanceof Boolean) {
                Map<String,Object> res = new HashMap<>();
                res.put("uid", subUids);
                res.put("success", true);
                res.put("transferability", transferability);
                return Arrays.asList(res);
            } else {
                throw new IllegalArgumentException("transferability must be bool");
            }
        }

        public Result getSubUserDepositHistory(Integer subUid) {
            if (subUid != null && subUid == -1) {
                throw new RuntimeException("Not found");
            }
            return new Result("done");
        }

        public Result postSubuserApikeyGenerate(String otpToken, int subUid, String note, String permission) {
            if (otpToken == null || otpToken.isEmpty() || note == null || note.isEmpty())
                throw new IllegalArgumentException("otp_token and note required");
            return new Result("done");
        }
    }

    static class Result {
        private final String value;
        Result(String v) { value = v; }
        public String printObject() { return value; }
    }

    DummySubuserClientPublic client;

    @BeforeEach
    public void setUp() {
        client = new DummySubuserClientPublic("public-key", "public-secret");
    }

    @Test
    public void testPostSetSubuserTransferabilityTrue() {
        List<Map<String, Object>> res = client.postSetSubuserTransferability("abcd", true);
        assertEquals(true, res.get(0).get("transferability"));
        assertEquals("abcd", res.get(0).get("uid"));
    }

    @Test
    public void testPostSetSubuserTransferabilityFalse() {
        List<Map<String, Object>> res = client.postSetSubuserTransferability("efgh", false);
        assertEquals(false, res.get(0).get("transferability"));
    }

    @Test
    public void testPostSetSubuserTransferabilityInvalid() {
        assertThrows(IllegalArgumentException.class, () ->
            client.postSetSubuserTransferability("efgh", 123));
    }

    @Test
    public void testPostSetSubuserTransferabilityNoUid() {
        assertThrows(IllegalArgumentException.class, () ->
            client.postSetSubuserTransferability(null, true));
    }

    @Test
    public void testGetSubUserDepositHistoryOk() {
        Result res = client.getSubUserDepositHistory(555);
        assertEquals("done", res.printObject());
    }

    @Test
    public void testGetSubUserDepositHistoryNotFound() {
        assertThrows(RuntimeException.class, () -> client.getSubUserDepositHistory(-1));
    }

    @Test
    public void testPostSubuserApikeyGenerateSuccess() {
        Result res = client.postSubuserApikeyGenerate("pub_otp", 999, "pub_note", "readWrite");
        assertEquals("done", res.printObject());
    }

    @Test
    public void testPostSubuserApikeyGenerateMissing() {
        assertThrows(IllegalArgumentException.class, () ->
            client.postSubuserApikeyGenerate("", 999, "", "readWrite")
        );
    }

    @Test
    public void testInit() {
        DummySubuserClientPublic c = new DummySubuserClientPublic();
        assertNull(c.apiKey);
        assertNull(c.secretKey);
    }
}