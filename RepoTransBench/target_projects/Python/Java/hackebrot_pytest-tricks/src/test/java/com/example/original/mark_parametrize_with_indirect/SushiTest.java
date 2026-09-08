package com.example.original.mark_parametrize_with_indirect;

import com.example.mark_parametrize_with_indirect.ConftestUtil;
import com.example.mark_parametrize_with_indirect.Restaurant;
import com.example.mark_parametrize_with_indirect.Sushi;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;

import java.util.List;
import java.util.stream.Stream;

import static org.assertj.core.api.Assertions.assertThat;

class SushiTest {
    static Stream<org.junit.jupiter.params.provider.Arguments> sushiAndSideDishProvider() {
        return Stream.of(
                org.junit.jupiter.params.provider.Arguments.of("Kappa Maki", "Edamame"),
                org.junit.jupiter.params.provider.Arguments.of("Kappa Maki", "Miso Soup"),
                org.junit.jupiter.params.provider.Arguments.of("Tamagoyaki", "Edamame"),
                org.junit.jupiter.params.provider.Arguments.of("Tamagoyaki", "Miso Soup"),
                org.junit.jupiter.params.provider.Arguments.of("Inarizushi", "Edamame"),
                org.junit.jupiter.params.provider.Arguments.of("Inarizushi", "Miso Soup")
        );
    }

    @ParameterizedTest(name="Sushi {0} with side dish {1}")
    @MethodSource("sushiAndSideDishProvider")
    void testFooshiServesVegetarianSushi(String sushiName, String sideDish) {
        Restaurant bar = ConftestUtil.fooshiBar();
        Sushi sushi = ConftestUtil.sushiByName(sushiName);
        assertThat(sushi.isVegetarian()).isTrue();
        assertThat(bar.getMenu()).contains(sushi.getName());
        assertThat(bar.getMenu()).contains(sideDish);
    }

    @Test
    void testSushi() {
        Sushi sushi = ConftestUtil.sushiByName("Kappa Maki");
        assertThat(sushi.getName()).isNotBlank();
        assertThat(sushi.getIngredients()).isNotEmpty();
    }
}