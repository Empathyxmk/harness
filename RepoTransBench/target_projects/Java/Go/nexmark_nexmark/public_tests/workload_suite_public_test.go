package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type WorkloadSuite struct {
	Category string
	QueryName string
}

func FromCategoryQueryName(category, query string) WorkloadSuite {
	return WorkloadSuite{Category: category, QueryName: query}
}

func (w WorkloadSuite) Suite() []WorkloadSuite {
	if w.Category == "oa" && w.QueryName == "all" {
		var wl []WorkloadSuite
		for i := 0; i < 10; i++ {
			wl = append(wl, WorkloadSuite{Category: "oa", QueryName: "q" + string('0'+i)})
		}
		return wl
	}
	return []WorkloadSuite{w}
}

func TestFromCategoryQueryNamePublic(t *testing.T) {
	suite := FromCategoryQueryName("cep", "q2")
	assert.NotNil(t, suite)
	suiteArr := suite.Suite()
	assert.False(t, len(suiteArr) == 0)
	assert.Equal(t, "q2", suiteArr[0].QueryName)
	assert.Equal(t, "cep", suiteArr[0].Category)
}

func TestFromCategoryQueryNameAllPublic(t *testing.T) {
	suite := FromCategoryQueryName("oa", "all")
	wl := suite.Suite()
	assert.NotNil(t, wl)
	assert.True(t, len(wl) > 5)
}