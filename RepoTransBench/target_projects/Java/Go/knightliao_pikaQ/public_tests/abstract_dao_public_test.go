package public_tests

import (
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
	return []*SimpleEntity{NewSimpleEntity(3), NewSimpleEntity(4)}
}
func (sd *SimpleDao) FindPaged(matchList []Match, orderList []Order, offset, limit int) []*SimpleEntity {
	return []*SimpleEntity{NewSimpleEntity(3), NewSimpleEntity(4)}
}
func (sd *SimpleDao) Count(matchList []Match) int { return 77 }
func (sd *SimpleDao) Page2(matchList []Match, page DaoPage) DaoPageResult[*SimpleEntity] {
	return DaoPageResult[*SimpleEntity]{Result: sd.Find(matchList, nil), TotalCount: 77}
}

func TestOrderMatchModify(t *testing.T) {
	dao := &SimpleDao{}
	order := dao.Order("otherCol", false)
	if order.GetColumn() != "otherCol" {
		t.Errorf("order.Column = %v, expected otherCol", order.GetColumn())
	}
	if order.IsAsc() {
		t.Error("order.Asc = true, expected false")
	}
	match := dao.Match("bar", 5)
	if match.GetColumn() != "bar" {
		t.Errorf("match.Column = %v, expected bar", match.GetColumn())
	}
	if match.GetValue() != 5 {
		t.Errorf("match.Value = %v, expected 5", match.GetValue())
	}
	modify := dao.Modify("baz", 8)
	if modify.GetColumn() != "baz" {
		t.Errorf("modify.Column = %v, expected baz", modify.GetColumn())
	}
	if modify.GetValue() != 8 {
		t.Errorf("modify.Value = %v, expected 8", modify.GetValue())
	}
}

func TestToList(t *testing.T) {
	dao := &SimpleDao{}
	empty := dao.ToList()
	if len(empty) != 0 {
		t.Errorf("empty list size = %d, expected 0", len(empty))
	}
	vals := dao.ToList("test", 42, 7.8, false)
	if len(vals) != 4 {
		t.Errorf("vals size = %d, expected 4", len(vals))
	}
	if vals[1] != 42 {
		t.Errorf("vals[1] = %v, expected 42", vals[1])
	}
	if vals[3] != false {
		t.Errorf("vals[3] = %v, expected false", vals[3])
	}
}

func TestPage2(t *testing.T) {
	dao := &SimpleDao{}
	page := DaoPage{PageNo: 2, PageSize: 10}
	result := dao.Page2([]Match{dao.Match("bar", 456)}, page)
	if result.Result == nil {
		t.Error("result.Result == nil")
	}
	if result.TotalCount != 77 {
		t.Errorf("result.TotalCount == %d, expected 77", result.TotalCount)
	}
}

func TestLikeBetweenGreaterLessExpressNotIncr(t *testing.T) {
	dao := &SimpleDao{}
	if dao.Like("otherStr") == nil {
		t.Error("Like(otherStr) == nil")
	}
	if dao.Between(2, 8) == nil {
		t.Error("Between(2,8) == nil")
	}
	if dao.GreaterThan(15) == nil {
		t.Error("GreaterThan(15) == nil")
	}
	if dao.LessThan(1) == nil {
		t.Error("LessThan(1) == nil")
	}
	if dao.Express() == nil {
		t.Error("Express() == nil")
	}
	if dao.Not("anotherVal") == nil {
		t.Error("Not('anotherVal') == nil")
	}
	if dao.Incr(10) == nil {
		t.Error("Incr(10) == nil")
	}
}