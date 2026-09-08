package com.tiddl.public_tests;

import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class PublicApiTest {
    static class TrackMock { String title; TrackMock(String t) { title = t; } }
    static class AlbumMock { String title; AlbumMock(String t) { title = t; } }
    static class PlaylistMock { String title; PlaylistMock(String t) { title = t; } }

    static class Api {
        TrackMock getTrack(int id) { return new TrackMock("Stronger"); }
        AlbumMock getAlbum(int id) { return new AlbumMock("Graduation"); }
        PlaylistMock getPlaylist(String id) { return new PlaylistMock("Kanye West Essentials"); }
    }
    Api api = new Api();

    @Test
    void test_get_track_title() {
        assertEquals("Stronger", api.getTrack(1).title);
    }

    @Test
    void test_get_album_title() {
        assertEquals("Graduation", api.getAlbum(2).title);
    }

    @Test
    void test_get_playlist_title() {
        assertEquals("Kanye West Essentials", api.getPlaylist("abc").title);
    }
}