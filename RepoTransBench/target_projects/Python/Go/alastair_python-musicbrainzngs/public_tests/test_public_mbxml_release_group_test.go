package public_tests

import (
	"encoding/xml"
	"strings"
	"testing"
)

type SecondaryType struct {
	XMLName xml.Name `xml:"secondary-type"`
	Text    string   `xml:",chardata"`
}

type ReleaseGroup struct {
	XMLName           xml.Name       `xml:"release-group"`
	ID                string         `xml:"id,attr"`
	Title             string         `xml:"title"`
	PrimaryType       string         `xml:"primary-type"`
	SecondaryTypeList struct {
		SecondaryTypes []SecondaryType `xml:"secondary-type"`
	} `xml:"secondary-type-list"`
}

type ReleaseGroupList struct {
	XMLName       xml.Name        `xml:"release-group-list"`
	ReleaseGroups []ReleaseGroup  `xml:"release-group"`
}

func TestReleaseGroupTypeParsingPublic(t *testing.T) {
	xmlInput := `
	<release-group-list count="1">
		<release-group id="0987abcd-1234-9876-bcd1-abcdefabcdef">
			<title>Public Test Album</title>
			<primary-type>MainType</primary-type>
			<secondary-type-list>
				<secondary-type>Soundtrack</secondary-type>
			</secondary-type-list>
		</release-group>
	</release-group-list>
	`
	var rgList ReleaseGroupList
	err := xml.Unmarshal([]byte(xmlInput), &rgList)
	if err != nil {
		t.Fatalf("could not parse xml: %v", err)
	}
	if len(rgList.ReleaseGroups) != 1 {
		t.Fatalf("expected 1 release-group, got %d", len(rgList.ReleaseGroups))
	}
	rg := rgList.ReleaseGroups[0]
	if rg.Title != "Public Test Album" {
		t.Errorf("expected title 'Public Test Album', got '%s'", rg.Title)
	}
	if rg.PrimaryType != "MainType" {
		t.Errorf("expected primary-type 'MainType', got '%s'", rg.PrimaryType)
	}
	var secondaries []string
	for _, s := range rg.SecondaryTypeList.SecondaryTypes {
		secondaries = append(secondaries, strings.TrimSpace(s.Text))
	}
	want := []string{"Soundtrack"}
	if len(secondaries) != len(want) || secondaries[0] != want[0] {
		t.Errorf("expected secondary types %v, got %v", want, secondaries)
	}
}