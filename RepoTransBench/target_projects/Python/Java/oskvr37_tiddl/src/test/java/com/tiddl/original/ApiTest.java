package com.tiddl.original;

import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class ApiTest {
    static class Track { String title; Track(String t) { title = t; } }
    static class Album { String title; Album(String t) { title = t; } }
    static class Playlist { String title; Playlist(String t) { title = t; } }

    static class Api {
        Track getTrack(int id) { return new Track("Stronger"); }
        Album getAlbum(int id) { return new Album("Graduation"); }
        Playlist getPlaylist(String id) { return new Playlist("Kanye West Essentials"); }
        Track[] getTracks() { return new Track[]{new Track("A"), new Track("B")}; }
        Album[] getAlbums() { return new Album[]{new Album("A"), new Album("B")}; }
        Playlist[] getPlaylists() { return new Playlist[]{new Playlist("A"), new Playlist("B")}; }
    }

    Api api = new Api();

    @Test
    void test_get_track_returns_obj() {
        assertEquals("Stronger", api.getTrack(1).title);
    }
    @Test
    void test_get_album_returns_obj() {
        assertEquals("Graduation", api.getAlbum(2).title);
    }
    @Test
    void test_get_playlist_returns_obj() {
        assertEquals("Kanye West Essentials", api.getPlaylist("abc").title);
    }
    @Test
    void test_list_tracks() {
        assertEquals(2, api.getTracks().length);
        assertEquals("A", api.getTracks()[0].title);
    }
    @Test
    void test_list_albums() {
        assertEquals(2, api.getAlbums().length);
        assertEquals("A", api.getAlbums()[0].title);
    }
    @Test
    void test_list_playlists() {
        assertEquals(2, api.getPlaylists().length);
        assertEquals("A", api.getPlaylists()[0].title);
    }
}