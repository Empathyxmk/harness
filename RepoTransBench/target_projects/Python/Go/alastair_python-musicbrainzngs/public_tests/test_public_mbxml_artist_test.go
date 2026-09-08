package public_tests

import (
	"encoding/xml"
	"testing"
)

type ArtistXML struct {
	XMLName xml.Name `xml:"artist"`
	ID      string   `xml:"id,attr"`
	Name    string   `xml:"name"`
	Gender  struct {
		ID   string `xml:"id,attr"`
		Text string `xml:",chardata"`
	} `xml:"gender"`
}

type ArtistListXML struct {
	XMLName xml.Name   `xml:"artist-list"`
	Artists []ArtistXML `xml:"artist"`
}

func TestParseArtistGenderPublic(t *testing.T) {
	xmlInput := `
	<artist-list count="2">
	  <artist id="rd6efc2ec-a7cb-433c-9e32-4640ad24e68a">
	    <name>John Doe</name>
	    <gender id="1">nonbinary</gender>
	  </artist>
	  <artist id="yd917559-c9eb-44da-bb74-ee9e3970b9ae">
	    <name>Jane Roe</name>
	    <gender id="2">female</gender>
	  </artist>
	</artist-list>
	`
	var al ArtistListXML
	if err := xml.Unmarshal([]byte(xmlInput), &al); err != nil {
		t.Fatalf("parse error: %v", err)
	}
	if len(al.Artists) != 2 {
		t.Errorf("expected 2 artists, got %d", len(al.Artists))
	}
	if al.Artists[0].Name != "John Doe" {
		t.Errorf("expected John Doe, got %s", al.Artists[0].Name)
	}
	if al.Artists[1].Name != "Jane Roe" {
		t.Errorf("expected Jane Roe, got %s", al.Artists[1].Name)
	}
	if al.Artists[0].Gender.Text != "nonbinary" {
		t.Errorf("expected gender nonbinary, got %s", al.Artists[0].Gender.Text)
	}
	if al.Artists[1].Gender.Text != "female" {
		t.Errorf("expected gender female, got %s", al.Artists[1].Gender.Text)
	}
}