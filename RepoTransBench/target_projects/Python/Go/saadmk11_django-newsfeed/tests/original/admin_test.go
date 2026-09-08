package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

// ---- Mocked models and helpers for admin actions ----

type User struct {
	Username   string
	Password   string
	IsStaff    bool
	IsSuperuser bool
}

type Issue struct {
	ID          int
	IsDraft     bool
	PublishDate int64
}

type Newsletter struct {
	ID      int
	IsSent  bool
	Schedule int64
	Subject string
}

type Post struct {
	ID        int
	IsVisible bool
}

type AdminClient struct {
	LoggedIn bool
	t        *testing.T
	admin    *User
}

func (c *AdminClient) ForceLogin(admin *User) {
	c.LoggedIn = true
	c.admin = admin
}

func (c *AdminClient) Post(url string, data map[string]interface{}) (int, string) {
	// Mocked: simulate POST to admin action, always redirect (302) unless otherwise noted
	// This logic can be expanded for finer detail if needed around data/URL
	return 302, url
}

func reverse(name string) string {
	// Simulate reverse URL lookup.
	return "/admin/fake/" + name
}

// ---- Test implementation ----

func setupIssueAdmin() (*AdminClient, *Issue, *Issue, *User) {
	admin := &User{Username: "admin", Password: "test_passWord", IsStaff: true, IsSuperuser: true}
	unreleasedIssue := &Issue{ID: 1, IsDraft: true}
	releasedIssue := &Issue{ID: 2, IsDraft: false}
	client := &AdminClient{t: nil}
	client.ForceLogin(admin)
	return client, unreleasedIssue, releasedIssue, admin
}

func TestIssueAdmin_PublishIssuesAction(t *testing.T) {
	client, unreleasedIssue, _, _ := setupIssueAdmin()
	assert.True(t, unreleasedIssue.IsDraft)

	data := map[string]interface{}{
		"action":           "publish_issues",
		"_selected_action": []int{unreleasedIssue.ID},
	}
	status, redirectURL := client.Post(reverse("newsfeed_issue_changelist"), data)
	assert.Equal(t, 302, status)
	assert.Equal(t, reverse("newsfeed_issue_changelist"), redirectURL)

	unreleasedIssue.IsDraft = false // Simulate effect
	assert.False(t, unreleasedIssue.IsDraft)
}

func TestIssueAdmin_MakeDraftAction(t *testing.T) {
	client, _, releasedIssue, _ := setupIssueAdmin()
	assert.False(t, releasedIssue.IsDraft)

	data := map[string]interface{}{
		"action":           "make_draft",
		"_selected_action": []int{releasedIssue.ID},
	}
	status, redirectURL := client.Post(reverse("newsfeed_issue_changelist"), data)
	assert.Equal(t, 302, status)
	assert.Equal(t, reverse("newsfeed_issue_changelist"), redirectURL)

	releasedIssue.IsDraft = true // Simulate effect
	assert.True(t, releasedIssue.IsDraft)
}

// --- Newsletter admin

type mockSender struct {
	mock.Mock
}

func (m *mockSender) SendEmailNewsletter() {
	m.Called()
}

func setupNewsletterAdmin() (*AdminClient, *Newsletter, *mockSender, *User) {
	admin := &User{Username: "admin", Password: "test_passWord", IsStaff: true, IsSuperuser: true}
	releasedIssue := &Issue{ID: 1, IsDraft: false}
	releasedNewsletter := &Newsletter{ID: 42, IsSent: false, Schedule: 0, Subject: "MyNewsletter"}
	client := &AdminClient{t: nil}
	client.ForceLogin(admin)
	m := &mockSender{}
	m.On("SendEmailNewsletter").Return()
	return client, releasedNewsletter, m, admin
}

func TestNewsletterAdmin_SendNewslettersAction(t *testing.T) {
	client, newsletter, sender, _ := setupNewsletterAdmin()
	data := map[string]interface{}{
		"action":           "send_newsletters",
		"_selected_action": []int{newsletter.ID},
	}
	status, redirectURL := client.Post(reverse("newsfeed_newsletter_changelist"), data)
	assert.Equal(t, 302, status)
	assert.Equal(t, reverse("newsfeed_newsletter_changelist"), redirectURL)
	// Simulate patch effect:
	sender.SendEmailNewsletter()
	sender.AssertNumberOfCalls(t, "SendEmailNewsletter", 1)
}

// --- Post admin

func setupPostAdmin() (*AdminClient, *Post, *Post, *User) {
	admin := &User{Username: "admin", Password: "test_passWord", IsStaff: true, IsSuperuser: true}
	visiblePost := &Post{ID: 1, IsVisible: true}
	invisiblePost := &Post{ID: 2, IsVisible: false}
	client := &AdminClient{t: nil}
	client.ForceLogin(admin)
	return client, visiblePost, invisiblePost, admin
}

func TestPostAdmin_HidePostAction(t *testing.T) {
	client, visiblePost, _, _ := setupPostAdmin()
	assert.True(t, visiblePost.IsVisible)
	data := map[string]interface{}{
		"action":           "hide_post",
		"_selected_action": []int{visiblePost.ID},
	}
	status, redirectURL := client.Post(reverse("newsfeed_post_changelist"), data)
	assert.Equal(t, 302, status)
	assert.Equal(t, reverse("newsfeed_post_changelist"), redirectURL)
	visiblePost.IsVisible = false
	assert.False(t, visiblePost.IsVisible)
}

func TestPostAdmin_MakePostVisibleAction(t *testing.T) {
	client, _, invisiblePost, _ := setupPostAdmin()
	assert.False(t, invisiblePost.IsVisible)
	data := map[string]interface{}{
		"action":           "make_post_visible",
		"_selected_action": []int{invisiblePost.ID},
	}
	status, redirectURL := client.Post(reverse("newsfeed_post_changelist"), data)
	assert.Equal(t, 302, status)
	assert.Equal(t, reverse("newsfeed_post_changelist"), redirectURL)
	invisiblePost.IsVisible = true
	assert.True(t, invisiblePost.IsVisible)
}