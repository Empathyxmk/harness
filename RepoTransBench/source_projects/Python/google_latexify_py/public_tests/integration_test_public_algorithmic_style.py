"""Public: End-to-end test cases of algorithmic style (different data)."""

import textwrap

from src.integration_tests import integration_utils


def test_fibonacci_algorithmic() -> None:
    def fib(n):
        if n <= 1:
            return n
        else:
            return fib(n - 1) + fib(n - 2)

    latex = textwrap.dedent(
        r"""
        \begin{algorithmic}
            \Function{fib}{$n$}
                \If{$n \leq 1$}
                    \State \Return $n$
                \Else
                    \State \Return $\mathrm{fib} \mathopen{}\left( n - 1 \mathclose{}\right) + \mathrm{fib} \mathopen{}\left( n - 2 \mathclose{}\right)$
                \EndIf
            \EndFunction
        \end{algorithmic}
        """  # noqa: E501
    ).strip()
    ipython_latex = (
        r"\begin{array}{l}"
        r" \mathbf{function} \ \mathrm{fib}(n) \\"
        r" \hspace{1em} \mathbf{if} \ n \leq 1 \\"
        r" \hspace{2em} \mathbf{return} \ n \\"
        r" \hspace{1em} \mathbf{else} \\"
        r" \hspace{2em} \mathbf{return} \ \mathrm{fib} \mathopen{}\left( n - 1 \mathclose{}\right) + \mathrm{fib} \mathopen{}\left( n - 2 \mathclose{}\right) \\"
        r" \hspace{1em} \mathbf{end \ if} \\"
        r" \mathbf{end \ function}"
        r" \end{array}"
    )
    integration_utils.check_algorithm(fib, latex, ipython_latex)


def test_count_digits_algorithmic() -> None:
    def count_digits(n):
        cnt = 0
        while n > 0:
            n //= 10
            cnt += 1
        return cnt

    latex = textwrap.dedent(
        r"""
        \begin{algorithmic}
            \Function{count\_digits}{$n$}
                \State $\mathrm{cnt} \gets 0$
                \While{$n > 0$}
                    \State $n \gets \left\lfloor\frac{n}{10}\right\rfloor$
                    \State $\mathrm{cnt} \gets \mathrm{cnt} + 1$
                \EndWhile
                \State \Return $\mathrm{cnt}$
            \EndFunction
        \end{algorithmic}
        """
    ).strip()
    ipython_latex = (
        r"\begin{array}{l}"
        r" \mathbf{function} \ \mathrm{count\_digits}(n) \\"
        r" \hspace{1em} \mathrm{cnt} \gets 0 \\"
        r" \hspace{1em} \mathbf{while} \ n > 0 \\"
        r" \hspace{2em} n \gets \left\lfloor\frac{n}{10}\right\rfloor \\"
        r" \hspace{2em} \mathrm{cnt} \gets \mathrm{cnt} + 1 \\"
        r" \hspace{1em} \mathbf{end \ while} \\"
        r" \hspace{1em} \mathbf{return} \ \mathrm{cnt} \\"
        r" \mathbf{end \ function}"
        r" \end{array}"
    )
    integration_utils.check_algorithm(count_digits, latex, ipython_latex)