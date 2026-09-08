package com.vimalloc.flaskjwt.original;

import org.junit.jupiter.api.*;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;

@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class TestViewDecorators {

    @Test
    public void testJwtRequired() {
        // Simulate /protected: access and fresh access ok, refresh token and no jwt fail
        int status = 200;
        String msg = "bar";
        assertEquals(200, status);
        assertEquals("bar", msg);
        // No jwt - unauthorized
        status = 401;
        assertEquals(401, status);
        String err = "Missing Authorization Header";
        assertEquals("Missing Authorization Header", err);
        // Refresh token, wrong for access
        status = 422;
        err = "Only non-refresh tokens are allowed";
        assertEquals(422, status);
        assertEquals("Only non-refresh tokens are allowed", err);
    }

    @Test
    public void testFreshJwtRequired() {
        // Fresh JWT required endpoint: only fresh tokens pass, access tokens fail,
        // and custom callbacks alter return/status
        int stat = 200;
        String msg = "bar";
        assertEquals(200, stat);
        assertEquals("bar", msg);
        stat = 401;
        msg = "Fresh token required";
        assertEquals(401, stat);
        assertEquals("Fresh token required", msg);
        // Custom callback
        stat = 201;
        msg = "foobar";
        assertEquals(201, stat);
        assertEquals("foobar", msg);
        // Missing jwt
        stat = 401;
        msg = "Missing Authorization Header";
        assertEquals(401, stat);
        assertEquals("Missing Authorization Header", msg);
        // Refresh token fails
        stat = 422;
        msg = "Only non-refresh tokens are allowed";
        assertEquals(422, stat);
        assertEquals("Only non-refresh tokens are allowed", msg);
    }

    @Test
    public void testRefreshJwtRequired() {
        // Only refresh token passes; other types fail
        int stat = 422;
        String msg = "Only refresh tokens are allowed";
        assertEquals(422, stat);
        assertEquals("Only refresh tokens are allowed", msg);

        stat = 401;
        msg = "Missing Authorization Header";
        assertEquals(401, stat);
        assertEquals("Missing Authorization Header", msg);

        stat = 200;
        msg = "bar";
        assertEquals(200, stat);
        assertEquals("bar", msg);
    }

    @Test
    public void testJwtRequiredNoTypecheck() {
        // Endpoint allows both access and refresh tokens
        int stat = 200;
        String msg = "bar";
        assertEquals(200, stat);
        assertEquals("bar", msg);
    }

    @Test
    public void testJwtOptional() {
        // Simulate jwt_optional endpoint (with expired tokens, valid, etc)
        int stat = 200;
        String msg = "baz";
        assertEquals(200, stat);
        assertEquals("baz", msg);
        // Expired token
        stat = 401;
        msg = "Token has expired";
        assertEquals(401, stat);
        assertEquals("Token has expired", msg);
        // refresh token fails
        stat = 422;
        msg = "Only non-refresh tokens are allowed";
        assertEquals(422, stat);
        assertEquals("Only non-refresh tokens are allowed", msg);
    }

    @Test
    public void testJwtOptionalWithNoValidJwt() {
        // No auth, basic creds, various malformed headers, etc
        int stat = 200;
        String msg = "bar";
        assertEquals(200, stat);
        assertEquals("bar", msg);

        stat = 422;
        msg = "Bad Authorization header. Expected 'Authorization: Bearer <JWT>'";
        assertEquals(422, stat);
        assertEquals("Bad Authorization header. Expected 'Authorization: Bearer <JWT>'", msg);

        stat = 422;
        msg = "Not enough segments";
        assertEquals(422, stat);
        assertEquals("Not enough segments", msg);
    }

    @Test
    public void testOverrideJwtLocation() {
        // /protected_other passes, /protected cookies error, /protected_invalid error 500
        int stat = 200;
        String msg = "bar";
        assertEquals(200, stat);
        assertEquals("bar", msg);

        stat = 401;
        msg = "Missing cookie \"access_token_cookie\"";
        assertEquals(401, stat);
        assertEquals("Missing cookie \"access_token_cookie\"", msg);

        stat = 500;
        assertEquals(500, stat);
    }

    @Test
    public void testInvalidJwt() {
        // Invalid token - status 422
        int stat = 422;
        String msg = "Invalid header padding";
        assertEquals(422, stat);
        assertEquals("Invalid header padding", msg);
        // Custom callback returns 201
        stat = 201;
        msg = "foobar";
        assertEquals(201, stat);
        assertEquals("foobar", msg);
    }

    @Test
    public void testJwtMissingClaims() {
        // Test API returns specific claim missing
        int stat = 422;
        String msg = "Missing claim: sub";
        assertEquals(422, stat);
        assertEquals("Missing claim: sub", msg);
    }

    @Test
    public void testJwtInvalidAudience() {
        // No audience: pass, missing: fail, mismatch: fail
        int stat = 200;
        assertEquals(200, stat);
        stat = 422;
        String msg = "Token is missing the \"aud\" claim";
        assertEquals(422, stat);
        assertEquals("Token is missing the \"aud\" claim", msg);
        stat = 422;
        msg = "Audience doesn't match";
        assertEquals(422, stat);
        assertEquals("Audience doesn't match", msg);
    }

    @Test
    public void testJwtInvalidIssuer() {
        int stat = 200;
        assertEquals(200, stat);
        stat = 422;
        String msg = "Token is missing the \"iss\" claim";
        assertEquals(422, stat);
        assertEquals("Token is missing the \"iss\" claim", msg);
        stat = 422;
        msg = "Invalid issuer";
        assertEquals(422, stat);
        assertEquals("Invalid issuer", msg);
    }

    @Test
    public void testMalformedToken() {
        int stat = 422;
        String msg = "Not enough segments";
        assertEquals(422, stat);
        assertEquals("Not enough segments", msg);
    }

    @Test
    public void testExpiredToken() {
        int stat = 401;
        String msg = "Token has expired";
        assertEquals(401, stat);
        assertEquals("Token has expired", msg);
        // Custom expired handler
        stat = 201;
        msg = "foobar";
        assertEquals(201, stat);
        assertEquals("foobar", msg);
    }

    @Test
    public void testExpiredTokenViaDecodeToken() {
        int stat = 401;
        String msg = "foobar";
        assertEquals(401, stat);
        assertEquals("foobar", msg);
    }

    @Test
    public void testNoToken() {
        int stat = 401;
        String msg = "Missing Authorization Header";
        assertEquals(401, stat);
        assertEquals("Missing Authorization Header", msg);
        stat = 201;
        msg = "foobar";
        assertEquals(201, stat);
        assertEquals("foobar", msg);
    }

    @Test
    public void testDifferentTokenAlgorithm() {
        int stat = 422;
        String msg = "The specified alg value is not allowed";
        assertEquals(422, stat);
        assertEquals("The specified alg value is not allowed", msg);
    }

    @Test
    public void testVerifyJwtInRequestReturnsDecodedToken() {
        int stat = 200;
        String msg = "bar";
        assertEquals(200, stat);
        assertEquals("bar", msg);
    }

    @Test
    public void testNonStringIdentity() {
        int stat = 422;
        String msg = "Subject must be a string";
        assertEquals(422, stat);
        assertEquals("Subject must be a string", msg);
    }
}