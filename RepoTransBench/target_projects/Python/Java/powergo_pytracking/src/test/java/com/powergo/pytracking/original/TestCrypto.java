package com.powergo.pytracking.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;
import java.nio.charset.StandardCharsets;

public class TestCrypto {

    private String hmacSha256(String message, String key) throws Exception {
        Mac mac = Mac.getInstance("HmacSHA256");
        mac.init(new SecretKeySpec(key.getBytes(StandardCharsets.UTF_8), "HmacSHA256"));
        byte[] rawHmac = mac.doFinal(message.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(rawHmac);
    }

    @Test
    void testHmacSha256() throws Exception {
        String secret = "s3cre7";
        String msg = "The quick brown fox jumps over the lazy dog";
        String actual = hmacSha256(msg, secret);
        // Python: base64.b64encode(hmac.new(b"s3cre7", b"The quick brown fox jumps over the lazy dog", hashlib.sha256).digest()).decode()
        assertEquals("r8iN68KYGv3ehDB1VZbJCmuIbAyCwXktA+H4dYhchuc=", actual);
    }

    @Test
    void testHmacSha256Empty() throws Exception {
        String secret = "";
        String msg = "";
        String actual = hmacSha256(msg, secret);
        // Python: base64.b64encode(hmac.new(b"", b"", hashlib.sha256).digest()).decode()
        assertEquals("thUXQpF1L3zegdbMhIbv71aLmlhNQnUOQx2kP/W9T2o=", actual);
    }
}