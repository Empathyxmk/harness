package original

import (
	"testing"
	"os"
	"github.com/stretchr/testify/assert"
	parsel "scrapy_parsel/parsel"
)

func loadAttack(attack string) (string, error) {
	b, err := os.ReadFile("../tests/xml_attacks/" + attack + ".xml")
	if err != nil {
		return "", err
	}
	return string(b), nil
}

func TestXMLAttackBillionLaughs(t *testing.T) {
	body, err := loadAttack("billion_laughs")
	assert.NoError(t, err)
	memoryBefore := parsel.CurrentMemoryUsage()
	sel := parsel.NewSelector(body)
	lolz := sel.CSS("lolz::text").Get()
	memoryAfter := parsel.CurrentMemoryUsage()
	memoryChange := memoryAfter - memoryBefore
	assert.LessOrEqual(t, memoryChange, 1024*1024, "Memory change should not exceed 1MiB")
	assert.Equal(t, "&lol9;", lolz)
}