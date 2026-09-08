package original

import (
	"reflect"
	"testing"
)

type SimpleEntity struct {
	ID int64
}

func (e *SimpleEntity) GetID() int64      { return e.ID }
func (e *SimpleEntity) SetID(id int64)    { e.ID = id }
func NewSimpleEntity(id int64) *SimpleEntity { return &SimpleEntity{ID: id} }

type Order struct {
	Column string
	Asc    bool
}
func (o Order) GetColumn() string { return o.Column }
func (o Order) IsAsc() bool       { return o.Asc }

type Match struct {
	Column string
	Value  interface{}
}
func (m Match) GetColumn() string    { return m.Column }
func (m Match) GetValue() interface{} { return m.Value }

type Modify struct {
	Column string
	Value  interface{}
}
func (m Modify) GetColumn() string    { return m.Column }
func (m Modify) GetValue() interface{} { return m.Value }

type DaoPage struct {
	PageNo   int
	PageSize int
}

type DaoPageResult[T any] struct {
	Result     []T
	TotalCount int
}

type AbstractDao struct{}

func (dao *AbstractDao) Order(column string, asc bool) Order {
	return Order{Column: column, Asc: asc}
}
func (dao *AbstractDao) Match(column string, value interface{}) Match {
	return Match{Column: column, Value: value}
}
func (dao *AbstractDao) Modify(column string, value interface{}) Modify {
	return Modify{Column: column, Value: value}
}
func (dao *AbstractDao) ToList(objs ...interface{}) []interface{} {
	return objs
}
func (dao *AbstractDao) Like(_ interface{}) interface{}        { return "like" }
func (dao *AbstractDao) Between(_ interface{}, _2 interface{}) interface{} { return "between" }
func (dao *AbstractDao) GreaterThan(_ interface{}) interface{} { return "greater" }
func (dao *AbstractDao) LessThan(_ interface{}) interface{}    { return "less" }
func (dao *AbstractDao) Express() interface{}                  { return "express" }
func (dao *AbstractDao) Not(_ interface{}) interface{}         { return "not" }
func (dao *AbstractDao) Incr(_ interface{}) interface{}        { return "incr" }

type SimpleDao struct {
	AbstractDao
}

func (sd *SimpleDao) Get(id int64) *SimpleEntity {
	return NewSimpleEntity(id)
}
func (sd *SimpleDao) Find(matchList []Match, orderList []Order) []*SimpleEntity {
	return []*SimpleEntity{NewSimpleEntity(1), NewSimpleEntity(2)}
}
func (sd *SimpleDao) FindPaged(matchList []Match, orderList []Order, offset, limit int) []*SimpleEntity {
	return []*SimpleEntity{NewSimpleEntity(1), NewSimpleEntity(2)}
}
func (sd *SimpleDao) Count(matchList []Match) int { return 42 }
func (sd *SimpleDao) Page2(matchList []Match, page DaoPage) DaoPageResult[*SimpleEntity] {
	return DaoPageResult[*SimpleEntity]{Result: sd.Find(matchList, nil), TotalCount: 42}
}

func TestOrderMatchModify(t *testing.T) {
	dao := &SimpleDao{}
	order := dao.Order("col", true)
	if order.GetColumn() != "col" {
		t.Errorf("order.Column = %v, expected col", order.GetColumn())
	}
	if !order.IsAsc() {
		t.Error("order.Asc = false, expected true")
	}
	match := dao.Match("foo", 1)
	if match.GetColumn() != "foo" {
		t.Errorf("match.Column = %v, expected foo", match.GetColumn())
	}
	if match.GetValue() != 1 {
		t.Errorf("match.Value = %v, expected 1", match.GetValue())
	}
	modify := dao.Modify("bar", 2)
	if modify.GetColumn() != "bar" {
		t.Errorf("modify.Column = %v, expected bar", modify.GetColumn())
	}
	if modify.GetValue() != 2 {
		t.Errorf("modify.Value = %v, expected 2", modify.GetValue())
	}
}

func TestToList(t *testing.T) {
	dao := &SimpleDao{}
	empty := dao.ToList()
	if len(empty) != 0 {
		t.Errorf("empty list size = %d, expected 0", len(empty))
	}
	vals := dao.ToList(1, "abc", 3.4)
	if len(vals) != 3 {
		t.Errorf("vals size = %d, expected 3", len(vals))
	}
	if vals[1] != "abc" {
		t.Errorf("vals[1] = %v, expected abc", vals[1])
	}
}

func TestPage2(t *testing.T) {
	dao := &SimpleDao{}
	page := DaoPage{PageNo: 1, PageSize: 20}
	result := dao.Page2([]Match{dao.Match("foo", 123)}, page)
	if result.Result == nil {
		t.Error("result.Result == nil")
	}
	if result.TotalCount != 42 {
		t.Errorf("result.TotalCount == %d, expected 42", result.TotalCount)
	}
}

func TestLikeBetweenGreaterLessExpressNotIncr(t *testing.T) {
	dao := &SimpleDao{}
	if dao.Like("str") == nil {
		t.Error("Like(str) == nil")
	}
	if dao.Between(1, 5) == nil {
		t.Error("Between(1,5) == nil")
	}
	if dao.GreaterThan(9) == nil {
		t.Error("GreaterThan(9) == nil")
	}
	if dao.LessThan(5) == nil {
		t.Error("LessThan(5) == nil")
	}
	if dao.Express() == nil {
		t.Error("Express() == nil")
	}
	if dao.Not("notVal") == nil {
		t.Error("Not('notVal') == nil")
	}
	if dao.Incr(3) == nil {
		t.Error("Incr(3) == nil")
	}
}