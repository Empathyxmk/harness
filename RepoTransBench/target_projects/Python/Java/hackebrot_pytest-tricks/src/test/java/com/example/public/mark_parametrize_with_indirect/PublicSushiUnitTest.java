package com.example.public.mark_parametrize_with_indirect;

import com.example.mark_parametrize_with_indirect.Sushi;
import com.example.mark_parametrize_with_indirect.Restaurant;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import java.util.List;
import static org.assertj.core.api.Assertions.*;

class PublicSushiUnitTest {

    @Test
    void testInitRaisesValueErrorIfIngredientsIsNull() {
        assertThatThrownBy(() -> new Sushi("California Roll", null)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void testInitRaisesValueErrorIfMenuIsNull() {
        assertThatThrownBy(() -> new Restaurant("Sushiland", "Tokyo", null)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void testInitWorksWithValidData() {
        Restaurant r = new Restaurant("Sushiland", "Osaka", List.of("Kani Nigiri"));
        assertThat(r.getMenu()).containsExactly("Kani Nigiri");
        Sushi s = new Sushi("Kani Nigiri", List.of("Crab", "Rice"));
        assertThat(s.getName()).isEqualTo("Kani Nigiri");
        assertThat(s.containsIngredient("Crab")).isTrue();
    }

    @Test
    void testContainsOperatorFalse() {
        Sushi sushi = new Sushi("Avocado Roll", List.of("Avocado", "Rice", "Nori"));
        assertThat(sushi.containsIngredient("Cucumber")).isFalse();
    }

    @Test
    void testContainsOperatorTrue() {
        Sushi sushi = new Sushi("Avocado Roll", List.of("Avocado", "Rice", "Nori"));
        assertThat(sushi.containsIngredient("Avocado")).isTrue();
    }

    static List<Object[]> isVegetarianCases() {
        return List.of(
                new Object[]{List.of("Avocado", "Rice", "Nori"), true},
                new Object[]{List.of("Tuna", "Rice", "Nori"), false},
                new Object[]{List.of("Egg", "Rice"), true},
                new Object[]{List.of("Shrimp", "Rice"), false}
        );
    }

    @ParameterizedTest
    @MethodSource("isVegetarianCasesProvider")
    void testIsVegetarianProperty(List<String> ingredients, boolean isVeg) {
        Sushi sushi = new Sushi("Custom Roll", ingredients);
        assertThat(sushi.isVegetarian()).isEqualTo(isVeg);
    }

    static java.util.stream.Stream<org.junit.jupiter.params.provider.Arguments> isVegetarianCasesProvider() {
        return isVegetarianCases().stream().map(arr -> org.junit.jupiter.params.provider.Arguments.of(arr[0], arr[1]));
    }
}