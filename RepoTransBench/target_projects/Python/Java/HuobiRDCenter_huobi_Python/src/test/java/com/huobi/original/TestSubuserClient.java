package com.huobi.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

public class TestSubuserClient {

    static class DummySubuserClient {
        String apiKey;
        String secretKey;

        DummySubuserClient() {}
        DummySubuserClient(String apiKey, String secretKey) {
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
            if (subUid != null && subUid == 0) {
                throw new RuntimeException("Not found");
            }
            return new Result("printed");
        }

        public Result postSubuserApikeyGenerate(String otpToken, int subUid, String note, String permission) {
            if (otpToken == null || otpToken.isEmpty() || note == null || note.isEmpty())
                throw new IllegalArgumentException("otp_token and note required");
            return new Result("printed");
        }
    }

    static class Result {
        private final String value;
        Result(String v) { value = v; }
        public String printObject() { return value; }
    }

    DummySubuserClient client;

    @BeforeEach
    public void setUp() {
        client = new DummySubuserClient("test-key", "test-secret");
    }

    @Test
    public void testPostSetSubuserTransferabilityTrue() {
        List<Map<String, Object>> res = client.postSetSubuserTransferability("1234", true);
        assertEquals(true, res.get(0).get("transferability"));
        assertEquals("1234", res.get(0).get("uid"));
    }

    @Test
    public void testPostSetSubuserTransferabilityFalse() {
        List<Map<String, Object>> res = client.postSetSubuserTransferability("999", false);
        assertEquals(false, res.get(0).get("transferability"));
    }

    @Test
    public void testPostSetSubuserTransferabilityInvalid() {
        assertThrows(IllegalArgumentException.class, () ->
            client.postSetSubuserTransferability("999", "invalid")
        );
    }

    @Test
    public void testPostSetSubuserTransferabilityNoUid() {
        assertThrows(IllegalArgumentException.class, () ->
            client.postSetSubuserTransferability(null, true)
        );
    }

    @Test
    public void testGetSubUserDepositHistoryOk() {
        Result res = client.getSubUserDepositHistory(100);
        assertEquals("printed", res.printObject());
    }

    @Test
    public void testGetSubUserDepositHistoryNotFound() {
        assertThrows(RuntimeException.class, () -> client.getSubUserDepositHistory(0));
    }

    @Test
    public void testPostSubuserApikeyGenerateSuccess() {
        Result res = client.postSubuserApikeyGenerate("otp", 123, "note", "readOnly");
        assertEquals("printed", res.printObject());
    }

    @Test
    public void testPostSubuserApikeyGenerateMissing() {
        assertThrows(IllegalArgumentException.class, () ->
            client.postSubuserApikeyGenerate(null, 123, "", "readOnly")
        );
    }

    @Test
    public void testInit() {
        DummySubuserClient c = new DummySubuserClient();
        assertNull(c.apiKey);
        assertNull(c.secretKey);
    }
}