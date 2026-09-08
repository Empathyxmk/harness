package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"flaskbabel"
)

func TestNumberFormattingBasics(t *testing.T) {
	app := &TestApp{}
	b := flaskbabel.NewBabel()
	b.InitApp(app)
	n := 1099

	withTestRequestContext(app, func() {
		assert.Equal(t, "1,099", b.FormatNumber(n))
		assert.Equal(t, "1,010.99", b.FormatDecimal(1010.99))
		assert.Equal(t, "$1,099.00", b.FormatCurrency(float64(n), "USD"))
		assert.Equal(t, "19%", b.FormatPercent(0.19))
		assert.Equal(t, "1E4", b.FormatScientific(10000))
	})
}