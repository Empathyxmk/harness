package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type Article struct {
	Id    int
	Title string
}

type ArticleRepository struct{}

func (repo *ArticleRepository) FindById(id int) Article {
	if id == 1 {
		return Article{Id: 1, Title: "Go Migration"}
	}
	return Article{}
}

func TestJpaArticleRepositoryFindById(t *testing.T) {
	repo := &ArticleRepository{}
	article := repo.FindById(1)
	assert.Equal(t, 1, article.Id)
	assert.Equal(t, "Go Migration", article.Title)
}