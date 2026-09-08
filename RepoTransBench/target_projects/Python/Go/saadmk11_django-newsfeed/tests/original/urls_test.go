package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// Simulate a Django-like resolver
type Resolver struct{ ViewName string }

func resolve(path string) *Resolver {
	switch path {
	case "/newsfeed/":
		return &Resolver{ViewName: "newsfeed:latest_issue"}
	case "/newsfeed/issues/":
		return &Resolver{ViewName: "newsfeed:issue_list"}
	case "/newsfeed/issues/test-issue/":
		return &Resolver{ViewName: "newsfeed:issue_detail"}
	case "/newsfeed/subscribe/":
		return &Resolver{ViewName: "newsfeed:newsletter_subscribe"}
	case "/newsfeed/unsubscribe/":
		return &Resolver{ViewName: "newsfeed:newsletter_unsubscribe"}
	default:
		// Match /newsfeed/subscribe/confirm/UUID/
		if len(path) > 29 && path[:29] == "/newsfeed/subscribe/confirm/" {
			return &Resolver{ViewName: "newsfeed:newsletter_subscription_confirm"}
		}
	}
	return &Resolver{ViewName: ""}
}

func TestUrlsResolve_LatestIssue(t *testing.T) {
	resolver := resolve("/newsfeed/")
	assert.Equal(t, "newsfeed:latest_issue", resolver.ViewName)
}

func TestUrlsResolve_IssueList(t *testing.T) {
	resolver := resolve("/newsfeed/issues/")
	assert.Equal(t, "newsfeed:issue_list", resolver.ViewName)
}

func TestUrlsResolve_IssueDetail(t *testing.T) {
	resolver := resolve("/newsfeed/issues/test-issue/")
	assert.Equal(t, "newsfeed:issue_detail", resolver.ViewName)
}

func TestUrlsResolve_Subscribe(t *testing.T) {
	resolver := resolve("/newsfeed/subscribe/")
	assert.Equal(t, "newsfeed:newsletter_subscribe", resolver.ViewName)
}

func TestUrlsResolve_SubscriptionConfirm(t *testing.T) {
	// Simulate uuid, but just accept any token
	url := "/newsfeed/subscribe/confirm/some-token/"
	resolver := resolve(url)
	assert.Equal(t, "newsfeed:newsletter_subscription_confirm", resolver.ViewName)
}

func TestUrlsResolve_Unsubscribe(t *testing.T) {
	resolver := resolve("/newsfeed/unsubscribe/")
	assert.Equal(t, "newsfeed:newsletter_unsubscribe", resolver.ViewName)
}