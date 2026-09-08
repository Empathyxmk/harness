package original

// DummyZAP mimics the interface needed for zapv2 components for isolated unit tests.
type DummyZAP struct {
	Base    string
	LastReq any
	Called  [][2]any
}

func NewDummyZAP() *DummyZAP {
	return &DummyZAP{Base: "BASE/", LastReq: nil, Called: make([][2]any, 0)}
}

func (dz *DummyZAP) Request(url string, params map[string]any) map[string]string {
	dz.LastReq = [2]any{url, params}
	return map[string]string{"value": "dummy"}
}

func (dz *DummyZAP) RequestArr(url string, params map[string]any) map[string]any {
	dz.Called = append(dz.Called, [2]any{url, params})
	return map[string]any{"value": "dummy"}
}