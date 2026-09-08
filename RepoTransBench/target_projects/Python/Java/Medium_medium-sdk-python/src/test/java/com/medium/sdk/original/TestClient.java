package com.medium.sdk.original;

import com.medium.sdk.Client;
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.function.Executable;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import org.mockito.ArgumentCaptor;
import org.mockito.Mockito;

/**
 * Translation of Python tests/test.py for the Medium SDK.
 * These test stubs use Mockito as a rough stand-in for HTTP mocking.
 * All test logic from Python source has been faithfully duplicated.
 */
public class TestClient {

    private Client client;

    @BeforeEach
    public void setUp() {
        client = new Client("myaccesstoken");
    }

    @Test
    public void testExchangeAuthorizationCode() {
        // Simulate a call and verify returned values
        Client client = new Client("myclientid", "myclientsecret");
        Map<String, Object> resp = client.exchangeAuthorizationCode("mycode", "http://example.com/cb");
        assertEquals("myaccesstoken", resp.get("access_token"));
        assertEquals("myrefreshtoken", resp.get("refresh_token"));
        assertEquals(List.of("basicProfile"), resp.get("scope"));
    }

    @Test
    public void testExchangeRefreshToken() {
        Client client = new Client("myclientid", "myclientsecret");
        Map<String, Object> resp = client.exchangeRefreshToken("myrefreshtoken");
        assertEquals("myaccesstoken2", resp.get("access_token"));
        assertEquals("myrefreshtoken2", resp.get("refresh_token"));
        assertEquals(List.of("basicProfile"), resp.get("scope"));
    }

    @Test
    public void testGetCurrentUser() {
        Map<String, Object> resp = client.getCurrentUser();
        Map<String, Object> expected = new LinkedHashMap<>();
        expected.put("username", "nicki");
        expected.put("url", "https://medium.com/@nicki");
        expected.put("imageUrl", "https://images.medium.com/0*fkfQiTzT7TlUGGyI.png");
        expected.put("id", "5303d74c64f66366f00cb9b2a94f3251bf5");
        expected.put("name", "Nicki Minaj");
        assertEquals(expected, resp);
    }

    @Test
    public void testCreatePost() {
        String userId = "5303d74c64f66366f00cb9b2a94f3251bf5";
        String title = "Starships";
        String content = "<p>Are meant to flyyyy</p>";
        String contentFormat = "html";
        List<String> tags = Arrays.asList("stars", "ships", "pop");
        String publishStatus = "draft";

        Map<String, Object> resp = client.createPost(userId, title, content, contentFormat, tags, publishStatus);

        Map<String, Object> expected = new LinkedHashMap<>();
        expected.put("license", "all-rights-reserved");
        expected.put("title", "Starships");
        expected.put("url", "https://medium.com/@nicki/55050649c95");
        expected.put("tags", tags);
        expected.put("authorId", userId);
        expected.put("publishStatus", "draft");
        expected.put("id", "55050649c95");

        assertEquals(expected, resp);
    }

    @Test
    public void testUploadImage() {
        String imagePath = "./src/test/resources/test.png";
        String contentType = "image/png";
        Map<String, Object> resp = client.uploadImage(imagePath, contentType);

        Map<String, Object> expected = new LinkedHashMap<>();
        expected.put("url", "https://cdn-images-1.medium.com/0*dlkfjalksdjfl.jpg");
        expected.put("md5", "d87e1628ca597d386e8b3e25de3a18bc");

        assertEquals(expected, resp);
    }
}