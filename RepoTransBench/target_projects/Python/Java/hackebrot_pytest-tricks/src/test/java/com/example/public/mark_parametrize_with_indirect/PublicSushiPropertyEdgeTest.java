package com.example.public.mark_parametrize_with_indirect;

import com.example.mark_parametrize_with_indirect.Sushi;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;

import java.util.List;
import java.util.stream.Stream;

import static org.assertj.core.api.Assertions.assertThat;

class PublicSushiPropertyEdgeTest {
    static Stream<org.junit.jupiter.params.provider.Arguments> edgeCasesProvider() {
        return Stream.of(
                org.junit.jupiter.params.provider.Arguments.of(List.of("Carrot", "Rice", "Nori"), true),
                org.junit.jupiter.params.provider.Arguments.of(List.of("Ham", "Rice"), true), // No recognized non-veg
                org.junit.jupiter.params.provider.Arguments.of(List.of("Tuna", "Rice"), false),
                org.junit.jupiter.params.provider.Arguments.of(List.of("Salmon", "Nori", "Rice"), false)
        );
    }

    @ParameterizedTest
    @MethodSource("edgeCasesProvider")
    void testPublicIsVegetarianEdgeCases(List<String> ingredients, boolean expected) {
        Sushi sushi = new Sushi("Edge Roll", ingredients);
        assertThat(sushi.isVegetarian()).isEqualTo(expected);
    }
}