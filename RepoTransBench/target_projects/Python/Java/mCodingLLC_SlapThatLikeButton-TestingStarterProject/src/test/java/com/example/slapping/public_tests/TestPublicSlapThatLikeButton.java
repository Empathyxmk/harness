package com.example.slapping.public_tests;

import com.example.slapping.*;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import static org.junit.jupiter.api.Assertions.*;

import java.util.stream.Stream;

class TestPublicSlapThatLikeButton {

    static Stream<org.junit.jupiter.params.provider.Arguments> provideSlapLike() {
        return Stream.of(
            org.junit.jupiter.params.provider.Arguments.of(LikeState.EMPTY, LikeState.LIKED),
            org.junit.jupiter.params.provider.Arguments.of(LikeState.LIKED, LikeState.EMPTY),
            org.junit.jupiter.params.provider.Arguments.of(LikeState.DISLIKED, LikeState.LIKED)
        );
    }

    @ParameterizedTest
    @MethodSource("provideSlapLike")
    void testPublicSlapLike(LikeState initial, LikeState expected) {
        assertSame(expected, SlapThatLikeButton.slap(initial, "l"));
    }

    static Stream<org.junit.jupiter.params.provider.Arguments> provideSlapDislike() {
        return Stream.of(
            org.junit.jupiter.params.provider.Arguments.of(LikeState.EMPTY, LikeState.DISLIKED),
            org.junit.jupiter.params.provider.Arguments.of(LikeState.LIKED, LikeState.DISLIKED),
            org.junit.jupiter.params.provider.Arguments.of(LikeState.DISLIKED, LikeState.EMPTY)
        );
    }

    @ParameterizedTest
    @MethodSource("provideSlapDislike")
    void testPublicSlapDislike(LikeState initial, LikeState expected) {
        assertSame(expected, SlapThatLikeButton.slap(initial, "d"));
    }

    @Test
    void testPublicSlapInvalidAction() {
        Exception ex = assertThrows(IllegalArgumentException.class, () ->
            SlapThatLikeButton.slap(LikeState.EMPTY, "x"));
        assertTrue(ex.getMessage().toLowerCase().contains("unknown"));
    }

    @Test
    void testPublicSlapManyLikeStreak() {
        // like->empty->like->empty->like: liked + "ll" = liked
        assertSame(LikeState.LIKED, SlapThatLikeButton.slapMany(LikeState.LIKED, "ll"));
    }

    @Test
    void testPublicSlapManyDislikeStreak() {
        // disliked->empty->disliked
        assertSame(LikeState.EMPTY, SlapThatLikeButton.slapMany(LikeState.DISLIKED, "d"));
        assertSame(LikeState.EMPTY, SlapThatLikeButton.slapMany(LikeState.EMPTY, "dd"));
    }

    static Stream<org.junit.jupiter.params.provider.Arguments> provideStatesTransitionsNewCases() {
        return Stream.of(
            org.junit.jupiter.params.provider.Arguments.of(LikeState.EMPTY, "dll", LikeState.LIKED),
            org.junit.jupiter.params.provider.Arguments.of(LikeState.LIKED, "dl", LikeState.DISLIKED),
            org.junit.jupiter.params.provider.Arguments.of(LikeState.LIKED, "dld", LikeState.EMPTY)
        );
    }

    @ParameterizedTest
    @MethodSource("provideStatesTransitionsNewCases")
    void testPublicStatesTransitionsNewCases(LikeState initial, String slapSeq, LikeState finalState) {
        assertSame(finalState, SlapThatLikeButton.slapMany(initial, slapSeq));
    }

    static Stream<org.junit.jupiter.params.provider.Arguments> provideStatesSlapManySimpleVariants() {
        return Stream.of(
            org.junit.jupiter.params.provider.Arguments.of(LikeState.EMPTY, "", LikeState.EMPTY),
            org.junit.jupiter.params.provider.Arguments.of(LikeState.EMPTY, "l", LikeState.LIKED),
            org.junit.jupiter.params.provider.Arguments.of(LikeState.LIKED, "d", LikeState.DISLIKED),
            org.junit.jupiter.params.provider.Arguments.of(LikeState.DISLIKED, "l", LikeState.LIKED)
        );
    }

    @ParameterizedTest
    @MethodSource("provideStatesSlapManySimpleVariants")
    void testPublicStatesSlapManySimpleVariants(LikeState initial, String slapSeq, LikeState finalState) {
        assertSame(finalState, SlapThatLikeButton.slapMany(initial, slapSeq));
    }

    static Stream<org.junit.jupiter.params.provider.Arguments> provideAutoSlapLikes() {
        return Stream.of(
            org.junit.jupiter.params.provider.Arguments.of(1, LikeState.LIKED),
            org.junit.jupiter.params.provider.Arguments.of(2, LikeState.EMPTY),
            org.junit.jupiter.params.provider.Arguments.of(3, LikeState.LIKED),
            org.junit.jupiter.params.provider.Arguments.of(6, LikeState.EMPTY)
        );
    }

    @ParameterizedTest
    @MethodSource("provideAutoSlapLikes")
    void testPublicAutoSlapLikes(int presses, LikeState expected) {
        assertSame(expected, SlapThatLikeButton.autoSlap(presses, "like"));
    }

    static Stream<org.junit.jupiter.params.provider.Arguments> provideAutoSlapDislikes() {
        return Stream.of(
            org.junit.jupiter.params.provider.Arguments.of(1, LikeState.DISLIKED),
            org.junit.jupiter.params.provider.Arguments.of(2, LikeState.EMPTY),
            org.junit.jupiter.params.provider.Arguments.of(3, LikeState.DISLIKED),
            org.junit.jupiter.params.provider.Arguments.of(6, LikeState.EMPTY)
        );
    }

    @ParameterizedTest
    @MethodSource("provideAutoSlapDislikes")
    void testPublicAutoSlapDislikes(int presses, LikeState expected) {
        assertSame(expected, SlapThatLikeButton.autoSlap(presses, "dislike"));
    }

    static Stream<String> provideAutoSlapInvalid() {
        return Stream.of("foo", "", null);
    }
    @ParameterizedTest
    @MethodSource("provideAutoSlapInvalid")
    void testPublicAutoSlapInvalid(String action) {
        Exception ex = assertThrows(IllegalArgumentException.class, () ->
            SlapThatLikeButton.autoSlap(1, action));
        assertTrue(ex.getMessage().toLowerCase().contains("invalid"));
    }
}