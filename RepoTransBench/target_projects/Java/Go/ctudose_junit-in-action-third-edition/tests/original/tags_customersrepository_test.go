package original

import (
	"testing"
)

type CustomerRepository struct {
	customers map[string]bool
}

func NewCustomerRepository() *CustomerRepository {
	return &CustomerRepository{customers: make(map[string]bool)}
}

func (r *CustomerRepository) Contains(name string) bool {
	return r.customers[name]
}
func (r *CustomerRepository) Persist(name string) {
	r.customers[name] = true
}

func TestCustomersRepositoryNonExistence(t *testing.T) {
	repo := NewCustomerRepository()
	exists := repo.Contains("John Smith")
	if exists {
		t.Errorf("expected John Smith not to exist in repository")
	}
}

func TestCustomersRepositoryPersistence(t *testing.T) {
	repo := NewCustomerRepository()
	repo.Persist("John Smith")
	if !repo.Contains("John Smith") {
		t.Errorf("expected John Smith to exist in repository after persist")
	}
}