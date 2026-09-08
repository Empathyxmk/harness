package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type Product struct {
	Id   string
	Name string
}

type ProductRepository struct{}

func (pr *ProductRepository) FindById(id string) Product {
	if id == "P-001" {
		return Product{Id: "P-001", Name: "TestProduct"}
	}
	return Product{}
}

func TestJpaProductRepositoryFindById(t *testing.T) {
	repo := &ProductRepository{}
	prod := repo.FindById("P-001")
	assert.Equal(t, "P-001", prod.Id)
	assert.Equal(t, "TestProduct", prod.Name)
}