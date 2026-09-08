package com.example.original.mark_parametrize_with_indirect;

import com.example.mark_parametrize_with_indirect.Sushi;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

class SushiPropertyEdgeTest {
    @Test
    void testIsVegetarianWithAllNonveg() {
        Sushi s = new Sushi("Mix", List.of("Crab", "Salmon", "Shrimp", "Tuna", "Rice"));
        assertThat(s.isVegetarian()).isFalse();
    }

    @Test
    void testIsVegetarianWithMixedCase() {
        Sushi s = new Sushi("Strange", List.of("crab", "salmon", "shrimp", "tuna"));
        assertThat(s.isVegetarian()).isTrue();
    }
}