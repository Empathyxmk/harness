package original

import (
    "testing"
    "github.com/yourusername/wikipediaapi"
)

func TestNamespaceEnumMembers(t *testing.T) {
    if wikipediaapi.NamespaceMAIN != 0 {
        t.Errorf("Expected NamespaceMAIN == 0, got %v", wikipediaapi.NamespaceMAIN)
    }
    if wikipediaapi.NamespaceUSER != 2 {
        t.Errorf("Expected NamespaceUSER == 2, got %v", wikipediaapi.NamespaceUSER)
    }
    if wikipediaapi.NamespaceCATEGORY != 14 {
        t.Errorf("Expected NamespaceCATEGORY == 14, got %v", wikipediaapi.NamespaceCATEGORY)
    }
    if wikipediaapi.NamespaceBOOK != 108 {
        t.Errorf("Expected NamespaceBOOK == 108, got %v", wikipediaapi.NamespaceBOOK)
    }
    if wikipediaapi.NamespaceGADGET != 2300 {
        t.Errorf("Expected NamespaceGADGET == 2300, got %v", wikipediaapi.NamespaceGADGET)
    }
}

func TestExtractFormatEnumMembers(t *testing.T) {
    if wikipediaapi.ExtractFormatWIKI != 1 {
        t.Errorf("Expected ExtractFormatWIKI == 1, got %v", wikipediaapi.ExtractFormatWIKI)
    }
    if wikipediaapi.ExtractFormatHTML != 2 {
        t.Errorf("Expected ExtractFormatHTML == 2, got %v", wikipediaapi.ExtractFormatHTML)
    }
}

func TestNamespace2IntWithEnum(t *testing.T) {
    if v := wikipediaapi.Namespace2int(wikipediaapi.NamespaceMAIN); v != 0 {
        t.Errorf("Expected Namespace2int(NamespaceMAIN)==0, got %v", v)
    }
    if v := wikipediaapi.Namespace2int(wikipediaapi.NamespaceCATEGORY); v != 14 {
        t.Errorf("Expected Namespace2int(NamespaceCATEGORY)==14, got %v", v)
    }
}

func TestNamespace2IntWithInt(t *testing.T) {
    if v := wikipediaapi.Namespace2int(42); v != 42 {
        t.Errorf("Expected Namespace2int(42)==42, got %v", v)
    }
    if v := wikipediaapi.Namespace2int(0); v != 0 {
        t.Errorf("Expected Namespace2int(0)==0, got %v", v)
    }
}

func TestInvalidNamespace2Int(t *testing.T) {
    if v := wikipediaapi.Namespace2int(wikipediaapi.NamespaceUSER_TALK); v != wikipediaapi.NamespaceUSER_TALK.Value() {
        t.Errorf("Expected Namespace2int(NamespaceUSER_TALK)==NamespaceUSER_TALK.Value(), got %v", v)
    }
}

func TestExtractFormatRepr(t *testing.T) {
    if n := wikipediaapi.ExtractFormatWIKI.Name(); n != "WIKI" {
        t.Errorf("Expected ExtractFormatWIKI.Name()==WIKI, got %v", n)
    }
    if n := wikipediaapi.ExtractFormatHTML.Name(); n != "HTML" {
        t.Errorf("Expected ExtractFormatHTML.Name()==HTML, got %v", n)
    }
}