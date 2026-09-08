package com.example.public.mark_parametrize_with_indirect;

import com.example.mark_parametrize_with_indirect.Sushi;
import com.example.mark_parametrize_with_indirect.ConftestUtil;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;
import java.util.stream.Stream;

import static org.assertj.core.api.Assertions.assertThat;

class PublicConftestPyIntegrationTest {

    static Map<String, List<String>> getRecipes() {
        return ConftestUtil.customRecipes();
    }

    static Stream<org.junit.jupiter.params.provider.Arguments> conftestRecipeProvider() {
        return Stream.of(
                org.junit.jupiter.params.provider.Arguments.of("spicytuna", List.of("tuna", "sriracha", "scallions")),
                org.junit.jupiter.params.provider.Arguments.of("rainbow", List.of("tuna", "avocado", "shrimp", "salmon"))
        );
    }
    @ParameterizedTest
    @MethodSource("conftestRecipeProvider")
    void testConftestPyRecipe(String sushiName, List<String> expectedIngredients) {
        Map<String, List<String>> recipes = getRecipes();
        Sushi roll = new Sushi(sushiName, recipes.get(sushiName));
        assertThat(roll.getIngredients()).isEqualTo(expectedIngredients);
    }
}