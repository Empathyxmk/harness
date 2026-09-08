package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class ViewsTest {

    // Simulate list of issues and posts for "listing" and "details" views

    static class Post {
        String title;
        boolean visible;
        public Post(String title, boolean visible) {
            this.title = title;
            this.visible = visible;
        }
    }
    static class Issue {
        String title;
        List<Post> posts = new ArrayList<>();
        public Issue(String title) { this.title = title; }
        void addPost(Post post) { posts.add(post); }
    }

    @Test
    void testIssueListView() {
        List<Issue> issues = Arrays.asList(
            new Issue("Issue 1"),
            new Issue("Issue 2")
        );
        assertEquals(2, issues.size());
        assertEquals("Issue 1", issues.get(0).title);
        assertEquals("Issue 2", issues.get(1).title);
    }

    @Test
    void testIssueDetailViewShowsPosts() {
        Issue issue = new Issue("Issue 2");
        Post post1 = new Post("Visible Post", true);
        Post post2 = new Post("Invisible Post", false);
        issue.addPost(post1);
        issue.addPost(post2);

        // Only show visible posts for detail view:
        List<Post> visiblePosts = new ArrayList<>();
        for (Post post : issue.posts) if (post.visible) visiblePosts.add(post);
        assertEquals(1, visiblePosts.size());
        assertEquals("Visible Post", visiblePosts.get(0).title);
    }
}