package com.example.original.mark_parametrize_with_indirect;

import com.example.mark_parametrize_with_indirect.Restaurant;
import com.example.mark_parametrize_with_indirect.Sushi;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;

import java.util.List;
import java.util.stream.Stream;

import static org.assertj.core.api.Assertions.*;

class SushiUnitTest {

    @Test
    void testRestaurantInitValid() {
        Restaurant r = new Restaurant("Foo", "Bar", List.of("Sushi1", "Sushi2"));
        assertThat(r.getName()).isEqualTo("Foo");
        assertThat(r.getLocation()).isEqualTo("Bar");
        assertThat(r.getMenu()).containsExactly("Sushi1", "Sushi2");
    }

    @Test
    void testRestaurantInitNoMenuRaises() {
        assertThatThrownBy(() -> new Restaurant("NoMenu", "Where", null))
                .isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void testSushiInitValid() {
        Sushi s = new Sushi("Veggie", List.of("Cucumber", "Rice"));
        assertThat(s.getName()).isEqualTo("Veggie");
        assertThat(s.getIngredients()).containsExactly("Cucumber", "Rice");
    }

    @Test
    void testSushiInitNoIngredientsRaises() {
        assertThatThrownBy(() -> new Sushi("Nothing", null)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void testSushiContainsTrue() {
        Sushi s = new Sushi("Veggie", List.of("Cucumber", "Rice"));
        assertThat(s.containsIngredient("Cucumber")).isTrue();
    }
    @Test
    void testSushiContainsFalse() {
        Sushi s = new Sushi("Veggie", List.of("Cucumber", "Rice"));
        assertThat(s.containsIngredient("Avocado")).isFalse();
    }

    static Stream<org.junit.jupiter.params.provider.Arguments> vegetarianIngredientsProvider() {
        return Stream.of(
                org.junit.jupiter.params.provider.Arguments.of(List.of("Rice", "Cucumber"), true),
                org.junit.jupiter.params.provider.Arguments.of(List.of("Rice", "Crab"), false),
                org.junit.jupiter.params.provider.Arguments.of(List.of("Salmon", "Rice"), false),
                org.junit.jupiter.params.provider.Arguments.of(List.of("Shrimp", "Rice"), false),
                org.junit.jupiter.params.provider.Arguments.of(List.of("Tuna", "Rice"), false),
                org.junit.jupiter.params.provider.Arguments.of(List.of("Egg", "Nori"), true)
        );
    }

    @ParameterizedTest
    @MethodSource("vegetarianIngredientsProvider")
    void testSushiIsVegetarian(List<String> ingredients, boolean expected) {
        Sushi s = new Sushi("Test", ingredients);
        assertThat(s.isVegetarian()).isEqualTo(expected);
    }
}