package com.example.original.mark_parametrize_with_indirect;

import com.example.mark_parametrize_with_indirect.ConftestUtil;
import com.example.mark_parametrize_with_indirect.Restaurant;
import com.example.mark_parametrize_with_indirect.Sushi;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Map;
import java.util.stream.Stream;

class ConftestPyIntegrationTest {
    @Test
    void testFooshiBarFixture() {
        Restaurant fooshiBar = ConftestUtil.fooshiBar();
        assertThat(fooshiBar).isInstanceOf(Restaurant.class);
        assertThat(fooshiBar.getName()).isEqualTo("Fooshi Bar");
        assertThat(fooshiBar.getMenu()).contains("Ebi Nigiri");
        assertThat(fooshiBar.getLocation()).isEqualTo("Buenos Aires");
        assertThat(fooshiBar.getMenu()).contains("Tamagoyaki");
    }

    @Test
    void testRecipesFixture() {
        Map<String, List<String>> recipes = ConftestUtil.recipes();
        assertThat(recipes).isInstanceOf(Map.class);
        assertThat(recipes).containsKey("Ebi Nigiri");
        assertThat(recipes.get("California Roll")).containsExactly("Rice", "Cucumber", "Avocado", "Crab");
    }

    static Stream<org.junit.jupiter.params.provider.Arguments> sushiFixtureParamProvider() {
        return Stream.of(
                org.junit.jupiter.params.provider.Arguments.of("California Roll"),
                org.junit.jupiter.params.provider.Arguments.of("Ebi Nigiri"),
                org.junit.jupiter.params.provider.Arguments.of("Tamagoyaki")
        );
    }
    @ParameterizedTest
    @MethodSource("sushiFixtureParamProvider")
    void testSushiFixtureParam(String sushiName) {
        Sushi s = ConftestUtil.sushiByName(sushiName);
        assertThat(s).isInstanceOf(Sushi.class);
        assertThat(s.getIngredients()).isInstanceOf(List.class);
        assertThat(s.getName()).isIn("California Roll", "Ebi Nigiri", "Tamagoyaki");
    }
}