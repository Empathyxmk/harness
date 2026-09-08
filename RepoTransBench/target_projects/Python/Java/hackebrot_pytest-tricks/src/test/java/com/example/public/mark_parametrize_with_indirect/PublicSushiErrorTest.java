package com.example.public.mark_parametrize_with_indirect;

import com.example.mark_parametrize_with_indirect.Sushi;
import com.example.mark_parametrize_with_indirect.Restaurant;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThatThrownBy;

class PublicSushiErrorTest {
    @Test
    void testPublicSushiInitRequiresIngredients() {
        assertThatThrownBy(() -> new Sushi("Rice Roll", null)).isInstanceOf(IllegalArgumentException.class);
    }
    @Test
    void testPublicRestaurantInitRequiresMenu() {
        assertThatThrownBy(() -> new Restaurant("Quick Sushi", "Naples", null)).isInstanceOf(IllegalArgumentException.class);
    }
}