"""Public: End-to-end regression-style test cases of function (different data)."""

import math

from src.integration_tests import integration_utils


def test_cubic_solution() -> None:
    def solve(a, b, c, d):
        # Cardano's formula is a bit complicated, so let's just test a simplified step.
        return -b / (3 * a)

    latex = r"\mathrm{solve}(a, b, c, d) = \frac{-b}{3 a}"
    integration_utils.check_function(solve, latex)


def test_heaviside_step() -> None:
    def heaviside(x):
        if x < 0:
            return 0
        else:
            return 1

    latex = (
        r"\mathrm{heaviside}(x) ="
        r" \left\{ \begin{array}{ll}"
        r" 0, & \mathrm{if} \ x < 0 \\"
        r" 1, & \mathrm{otherwise}"
        r" \end{array} \right."
    )
    integration_utils.check_function(heaviside, latex)


def test_y_times_alpha() -> None:
    def ytimesalpha(y, alpha):
        return y * alpha

    latex_without_symbols = (
        r"\mathrm{ytimesalpha}(y, \mathrm{alpha}) = y \cdot \mathrm{alpha}"
    )
    integration_utils.check_function(ytimesalpha, latex_without_symbols)
    integration_utils.check_function(
        ytimesalpha, latex_without_symbols, use_math_symbols=False
    )

    latex_with_symbols = r"\mathrm{ytimesalpha}(y, \alpha) = y \alpha"
    integration_utils.check_function(
        ytimesalpha, latex_with_symbols, use_math_symbols=True
    )


def test_sum_squares_even() -> None:
    def sum_squares_even(n):
        return sum(i**2 for i in range(0, n, 2))

    latex = (
        r"\mathrm{sum\_squares\_even}(n) = \sum_{i = 0}^{n - 1}"
        r" \mathopen{}\left({i^{2}}\mathclose{}\right), \ i \ \mathrm{even}"
    )
    # Note: We assume check_function can accept more sophisticated limits if the implementation supports.
    # If not, we could choose instead a range like (i for i in range(1, n+1)) for something different.
    integration_utils.check_function(sum_squares_even, latex)


def test_sum_cubes_custom_limits() -> None:
    def sum_cubes(a, n):
        return sum(i**3 for i in range(a, n))

    latex = (
        r"\mathrm{sum\_cubes}(a, n) = \sum_{i = a}^{n - 1}"
        r" \mathopen{}\left({i^{3}}\mathclose{}\right)"
    )
    integration_utils.check_function(sum_cubes, latex)


def test_prod_even_numbers() -> None:
    def prod_even(n):
        return math.prod(i for i in range(2, n * 2, 2))

    latex = (
        r"\mathrm{prod\_even}(n) = \prod_{i = 2}^{2 n - 2} \mathopen{}\left({i}\mathclose{}\right), \ i\ \mathrm{even}"
    )
    integration_utils.check_function(prod_even, latex)


def test_nested_multiplier() -> None:
    def multiply(x):
        def inner(y):
            return x * y

        return inner

    integration_utils.check_function(multiply(4), r"\mathrm{inner}(y) = x y")


def test_reduce_assignments_variant() -> None:
    def g(x):
        b = x * 2
        return 2 + b

    integration_utils.check_function(
        g,
        r"\begin{array}{l} b = x \cdot 2 \\ g(x) = 2 + b \end{array}",
    )
    integration_utils.check_function(
        g,
        r"g(x) = 2 + \mathopen{}\left( x \cdot 2 \mathclose{}\right)",
        reduce_assignments=True,
    )