// Code generated from src/integration_tests/algorithmic_style_test.py
package original

import (
	"testing"

	"github.com/yourusername/googlelatexify/integration_utils"
	"strings"
)

func TestFactorial(t *testing.T) {
	fact := func(n int) int {
		if n == 0 {
			return 1
		} else {
			return n * fact(n-1)
		}
	}

	latex := strings.TrimSpace(`
        \begin{algorithmic}
            \Function{fact}{$n$}
                \If{$n = 0$}
                    \State \Return $1$
                \Else
                    \State \Return $n \cdot \mathrm{fact} \mathopen{}\left( n - 1 \mathclose{}\right)$
                \EndIf
            \EndFunction
        \end{algorithmic}
	`)
	ipythonLatex := `\begin{array}{l}` +
		` \mathbf{function} \ \mathrm{fact}(n) \\` +
		` \hspace{1em} \mathbf{if} \ n = 0 \\` +
		` \hspace{2em} \mathbf{return} \ 1 \\` +
		` \hspace{1em} \mathbf{else} \\` +
		` \hspace{2em} \mathbf{return} \ n \cdot \mathrm{fact} \mathopen{}\left( n - 1 \mathclose{}\right) \\` +
		` \hspace{1em} \mathbf{end \ if} \\` +
		` \mathbf{end \ function}` +
		` \end{array}`

	integration_utils.CheckAlgorithm(t, fact, latex, ipythonLatex)
}

func TestCollatz(t *testing.T) {
	collatz := func(n int) int {
		iterations := 0
		for n > 1 {
			if n%2 == 0 {
				n = n / 2
			} else {
				n = 3*n + 1
			}
			iterations = iterations + 1
		}
		return iterations
	}

	latex := strings.TrimSpace(`
        \begin{algorithmic}
            \Function{collatz}{$n$}
                \State $\mathrm{iterations} \gets 0$
                \While{$n > 1$}
                    \If{$n \mathbin{\%} 2 = 0$}
                        \State $n \gets \left\lfloor\frac{n}{2}\right\rfloor$
                    \Else
                        \State $n \gets 3 n + 1$
                    \EndIf
                    \State $\mathrm{iterations} \gets \mathrm{iterations} + 1$
                \EndWhile
                \State \Return $\mathrm{iterations}$
            \EndFunction
        \end{algorithmic}
    `)
	ipythonLatex := `\begin{array}{l}` +
		` \mathbf{function} \ \mathrm{collatz}(n) \\` +
		` \hspace{1em} \mathrm{iterations} \gets 0 \\` +
		` \hspace{1em} \mathbf{while} \ n > 1 \\` +
		` \hspace{2em} \mathbf{if} \ n \mathbin{\%} 2 = 0 \\` +
		` \hspace{3em} n \gets \left\lfloor\frac{n}{2}\right\rfloor \\` +
		` \hspace{2em} \mathbf{else} \\` +
		` \hspace{3em} n \gets 3 n + 1 \\` +
		` \hspace{2em} \mathbf{end \ if} \\` +
		` \hspace{2em} \mathrm{iterations} \gets \mathrm{iterations} + 1 \\` +
		` \hspace{1em} \mathbf{end \ while} \\` +
		` \hspace{1em} \mathbf{return} \ \mathrm{iterations} \\` +
		` \mathbf{end \ function}` +
		` \end{array}`

	integration_utils.CheckAlgorithm(t, collatz, latex, ipythonLatex)
}