package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type MyPublicModel struct {
	ID   string
	Name string
	Age  int
}

type InMemoryRepository struct {
	data map[string]MyPublicModel
}

func NewInMemoryRepository() *InMemoryRepository {
	return &InMemoryRepository{
		data: make(map[string]MyPublicModel),
	}
}

func (r *InMemoryRepository) Save(obj MyPublicModel) {
	if obj.ID == "" {
		obj.ID = obj.Name // Simulate autogen id
	}
	r.data[obj.ID] = obj
}

func (r *InMemoryRepository) Get(id string) *MyPublicModel {
	if val, ok := r.data[id]; ok {
		return &val
	}
	return nil
}

func (r *InMemoryRepository) All() []MyPublicModel {
	objs := make([]MyPublicModel, 0, len(r.data))
	for _, o := range r.data {
		objs = append(objs, o)
	}
	return objs
}

func TestPublicModelFields(t *testing.T) {
	obj := MyPublicModel{Name: "Alice Wonderland", Age: 35}
	assert.Equal(t, "Alice Wonderland", obj.Name)
	assert.Equal(t, 35, obj.Age)
}

func TestPublicModelUpdateFields(t *testing.T) {
	obj := MyPublicModel{Name: "Bob Builder", Age: 44}
	obj.Name = "Bobby"
	obj.Age = 45
	assert.Equal(t, "Bobby", obj.Name)
	assert.Equal(t, 45, obj.Age)
}

func TestPublicModelRepository(t *testing.T) {
	repo := NewInMemoryRepository()
	obj := MyPublicModel{Name: "Charlie Delta", Age: 27}
	repo.Save(obj)
	found := repo.Get(obj.Name) // using Name as fake ID
	assert.NotNil(t, found)
	assert.Equal(t, "Charlie Delta", found.Name)
	assert.Equal(t, 27, found.Age)
	allObjs := repo.All()
	var foundAny bool
	for _, o := range allObjs {
		if o.Name == "Charlie Delta" && o.Age == 27 {
			foundAny = true
		}
	}
	assert.True(t, foundAny)
}