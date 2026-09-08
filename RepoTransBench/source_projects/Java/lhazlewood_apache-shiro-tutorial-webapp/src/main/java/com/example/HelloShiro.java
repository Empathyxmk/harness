package com.example;

/**
 * Example class to demonstrate Shiro login, logout, and simple message logic.
 */
public class HelloShiro {
    private boolean authenticated = false;
    private String user = null;

    public boolean login(String username, String password) {
        // For demonstration: only one user is valid
        if ("admin".equals(username) && "adminpass".equals(password)) {
            authenticated = true;
            user = username;
            return true;
        } else {
            authenticated = false;
            user = null;
            return false;
        }
    }

    public void logout() {
        authenticated = false;
        user = null;
    }

    public boolean isAuthenticated() {
        return authenticated;
    }

    public String getUser() {
        return user;
    }

    public String getWelcomeMessage() {
        if (!authenticated) {
            return "Please log in.";
        }
        switch (user) {
            case "admin":
                return "Welcome, admin!";
            default:
                return "Welcome, " + user + "!";
        }
    }
}