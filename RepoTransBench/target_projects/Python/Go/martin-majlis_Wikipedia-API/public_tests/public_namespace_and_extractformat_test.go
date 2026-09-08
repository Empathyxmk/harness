package public_tests

import (
    "testing"
    "github.com/yourusername/wikipediaapi"
)

func TestPublicNamespaceEnumMembers(t *testing.T) {
    if wikipediaapi.NamespaceTALK != 1 {
        t.Errorf("Expected NamespaceTALK == 1, got %v", wikipediaapi.NamespaceTALK)
    }
    if wikipediaapi.NamespacePROJECT != 4 {
        t.Errorf("Expected NamespacePROJECT == 4, got %v", wikipediaapi.NamespacePROJECT)
    }
    if wikipediaapi.NamespaceFILE != 6 {
        t.Errorf("Expected NamespaceFILE == 6, got %v", wikipediaapi.NamespaceFILE)
    }
    if wikipediaapi.NamespacePORTAL != 100 {
        t.Errorf("Expected NamespacePORTAL == 100, got %v", wikipediaapi.NamespacePORTAL)
    }
    if wikipediaapi.NamespaceGADGET_TALK != 2301 {
        t.Errorf("Expected NamespaceGADGET_TALK == 2301, got %v", wikipediaapi.NamespaceGADGET_TALK)
    }
}

func TestPublicExtractFormatEnumMembers(t *testing.T) {
    if wikipediaapi.ExtractFormatHTML != 2 {
        t.Errorf("Expected ExtractFormatHTML == 2, got %v", wikipediaapi.ExtractFormatHTML)
    }
    if wikipediaapi.ExtractFormatWIKI != 1 {
        t.Errorf("Expected ExtractFormatWIKI == 1, got %v", wikipediaapi.ExtractFormatWIKI)
    }
}

func TestPublicNamespace2intWithEnumOther(t *testing.T) {
    if v := wikipediaapi.Namespace2int(wikipediaapi.NamespaceFILE); v != 6 {
        t.Errorf("Expected Namespace2int(NamespaceFILE)==6, got %v", v)
    }
    if v := wikipediaapi.Namespace2int(wikipediaapi.NamespacePORTAL); v != 100 {
        t.Errorf("Expected Namespace2int(NamespacePORTAL)==100, got %v", v)
    }
}

func TestPublicNamespace2intWithDifferentInt(t *testing.T) {
    if v := wikipediaapi.Namespace2int(99); v != 99 {
        t.Errorf("Expected Namespace2int(99)==99, got %v", v)
    }
    if v := wikipediaapi.Namespace2int(6); v != 6 {
        t.Errorf("Expected Namespace2int(6)==6, got %v", v)
    }
}

func TestPublicInvalidNamespace2intOther(t *testing.T) {
    if v := wikipediaapi.Namespace2int(wikipediaapi.NamespacePROJECT_TALK); v != wikipediaapi.NamespacePROJECT_TALK.Value() {
        t.Errorf("Expected Namespace2int(NamespacePROJECT_TALK)==NamespacePROJECT_TALK.Value(), got %v", v)
    }
}

func TestPublicExtractFormatReprOther(t *testing.T) {
    if n := wikipediaapi.ExtractFormatHTML.Name(); n != "HTML" {
        t.Errorf("Expected ExtractFormatHTML.Name()==HTML, got %v", n)
    }
    if n := wikipediaapi.ExtractFormatWIKI.Name(); n != "WIKI" {
        t.Errorf("Expected ExtractFormatWIKI.Name()==WIKI, got %v", n)
    }
}