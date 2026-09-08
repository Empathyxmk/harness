package com.example.public.mark_parametrize_with_indirect;

import com.example.mark_parametrize_with_indirect.Sushi;
import com.example.mark_parametrize_with_indirect.ConftestUtil;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import java.util.List;
import static org.assertj.core.api.Assertions.assertThat;

class PublicSushiTest {
    @ParameterizedTest
    @ValueSource(strings = {"rainbow", "spicytuna"})
    void testRecipeExistsForRoll(String roll) {
        var recipes = ConftestUtil.customRecipes();
        assertThat(recipes.containsKey(roll)).isTrue();
        Sushi s = new Sushi(roll, recipes.get(roll));
        assertThat(s.getIngredients()).isEqualTo(recipes.get(roll));
    }
}