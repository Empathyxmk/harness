package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class FormsTest {

    // Simulate the forms for subscription

    static class NewsletterSubscriptionForm {
        private String email;
        public NewsletterSubscriptionForm(String email) { this.email = email; }
        public boolean isValid() { return email != null && email.contains("@"); }
        public String getEmail() { return email; }
    }

    static class NewsletterUnsubscribeForm {
        private String email;
        public NewsletterUnsubscribeForm(String email) { this.email = email; }
        public boolean isValid() { return email != null && email.contains("@"); }
        public String getEmail() { return email; }
    }

    @Test
    void testValidEmailSubscribeForm() {
        NewsletterSubscriptionForm form = new NewsletterSubscriptionForm("john@example.com");
        assertTrue(form.isValid());
        assertEquals("john@example.com", form.getEmail());
    }

    @Test
    void testInvalidEmailSubscribeForm() {
        NewsletterSubscriptionForm form = new NewsletterSubscriptionForm("foo");
        assertFalse(form.isValid());
    }

    @Test
    void testValidEmailUnsubscribeForm() {
        NewsletterUnsubscribeForm form = new NewsletterUnsubscribeForm("jane@example.com");
        assertTrue(form.isValid());
        assertEquals("jane@example.com", form.getEmail());
    }

    @Test
    void testInvalidUnsubscribeForm() {
        NewsletterUnsubscribeForm form = new NewsletterUnsubscribeForm("");
        assertFalse(form.isValid());
        NewsletterUnsubscribeForm form2 = new NewsletterUnsubscribeForm(null);
        assertFalse(form2.isValid());
    }
}