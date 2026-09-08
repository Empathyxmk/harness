package com.example.original.mark_parametrize_with_indirect;

import com.example.mark_parametrize_with_indirect.Restaurant;
import com.example.mark_parametrize_with_indirect.Sushi;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.Collections;

class SushiErrorTest {
    @Test
    void testRestaurantEmptyMenuListRaises() {
        // Should throw error on empty menu
        assertThatThrownBy(() -> new Restaurant("Foo", "Bar", Collections.emptyList()))
                .isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void testSushiEmptyIngredientsListRaises() {
        assertThatThrownBy(() -> new Sushi("Foo", Collections.emptyList()))
                .isInstanceOf(IllegalArgumentException.class);
    }
}