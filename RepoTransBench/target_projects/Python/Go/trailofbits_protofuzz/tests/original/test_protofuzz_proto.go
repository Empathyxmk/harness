// Code generated manually for test coverage
// This just creates appropriate message types matching test.proto, so importProtoModule works.

package original

type Person struct {
	Name   string
	Id     int32
	Email  *string
	Phone  []*PhoneNumber
}

type PhoneNumber struct {
	Number string
	Type   *PhoneType
}

type PhoneType int32

const (
	PhoneType_MOBILE PhoneType = 0
	PhoneType_HOME   PhoneType = 1
	PhoneType_WORK   PhoneType = 2
)

type Other struct {
	Foo   string
	Index int32
}

type AddressBook struct {
	Other  *Other
	Person []*Person
}

type Descriptor struct {
	Fields []interface{}
}