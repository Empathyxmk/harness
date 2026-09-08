package public_tests

import (
	"testing"

	"scrapinghub_adblockparser/adblockparser"
)

func adblockRulesInstance() adblockparser.AdblockRules {
	rules := []string{
		"/track.js$script",
		"/log.gif$image",
		"||adnetwork.com^$third-party",
		"@@||safe.com/banner.gif$image",
	}
	return adblockparser.NewAdblockRules(rules)
}

func TestPublicBlockScript(t *testing.T) {
	adp := adblockRulesInstance()
	if !adp.ShouldBlock("http://another.com/track.js", map[string]interface{}{"script": true}) {
		t.Error("Should block track.js with script param")
	}
	if adp.ShouldBlock("http://another.com/track.js", map[string]interface{}{"image": true}) {
		t.Error("Should not block track.js with image param")
	}
}

func TestPublicBlockImage(t *testing.T) {
	adp := adblockRulesInstance()
	if adp.ShouldBlock("http://foo.com/track.gif", map[string]interface{}{"image": true}) {
		t.Error("Should not block track.gif")
	}
	if !adp.ShouldBlock("http://foo.com/log.gif", map[string]interface{}{"image": true}) {
		t.Error("Should block log.gif")
	}
}

func TestPublicThirdParty(t *testing.T) {
	adp := adblockRulesInstance()
	if adp.ShouldBlock("http://x.yz/ad.js", map[string]interface{}{"third-party": true}) {
		t.Error("Should not block x.yz/ad.js as third-party")
	}
	if !adp.ShouldBlock("http://adnetwork.com/adv_banner.jpg", map[string]interface{}{"third-party": true}) {
		t.Error("Should block adnetwork.com/adv_banner.jpg as third-party")
	}
}

func TestPublicException(t *testing.T) {
	adp := adblockRulesInstance()
	if adp.ShouldBlock("http://safe.com/banner.gif", map[string]interface{}{"image": true}) {
		t.Error("Should not block safe.com/banner.gif")
	}
}