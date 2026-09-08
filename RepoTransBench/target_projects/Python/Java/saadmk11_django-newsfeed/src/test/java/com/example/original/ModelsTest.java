package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class ModelsTest {

    static class Post {
        int id;
        String title;
        boolean visible;

        public Post(int id, String title, boolean visible) {
            this.id = id;
            this.title = title;
            this.visible = visible;
        }

        public String toString() {
            return title;
        }
    }

    static class Issue {
        int id;
        String title;
        String description;
        int issueType; // 0/1/2, etc.
        boolean published;
        List<Post> posts = new ArrayList<>();

        public Issue(int id, String title, String description, int issueType, boolean published) {
            this.id = id;
            this.title = title;
            this.description = description;
            this.issueType = issueType;
            this.published = published;
        }

        void addPost(Post post) { posts.add(post); }
        public String toString() { return title; }
    }

    static class Subscriber {
        int id;
        String email;
        boolean isActive;
        boolean isVerified;
        String verificationCode;

        public Subscriber(int id, String email, boolean isActive, boolean isVerified, String verificationCode) {
            this.id = id;
            this.email = email;
            this.isActive = isActive;
            this.isVerified = isVerified;
            this.verificationCode = verificationCode;
        }

        public String toString() { return email; }
    }

    @Test
    void testPostModelString() {
        Post post = new Post(1, "My Post", true);
        assertEquals("My Post", post.toString());
    }

    @Test
    void testIssueModelString() {
        Issue issue = new Issue(2, "My Issue", "Some description", 1, true);
        assertEquals("My Issue", issue.toString());
    }

    @Test
    void testSubscriberModelString() {
        Subscriber subscriber = new Subscriber(1, "user@example.com", true, true, "code123");
        assertEquals("user@example.com", subscriber.toString());
    }

    @Test
    void testIssueAddPost() {
        Issue issue = new Issue(1, "Issue A", "desc", 1, true);
        assertEquals(0, issue.posts.size());
        Post post = new Post(10, "Post X", true);
        issue.addPost(post);
        assertEquals(1, issue.posts.size());
        assertEquals(post, issue.posts.get(0));
    }

    @Test
    void testSubscriberActivationFlags() {
        Subscriber sub = new Subscriber(12, "active@example.com", true, false, "abcd");
        assertTrue(sub.isActive);
        assertFalse(sub.isVerified);
        Subscriber sub2 = new Subscriber(13, "inactive@example.com", false, false, "dcba");
        assertFalse(sub2.isActive);
    }
}