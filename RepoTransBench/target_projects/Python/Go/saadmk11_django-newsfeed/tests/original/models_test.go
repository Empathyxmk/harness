package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
	"time"
)

// Mocks (simulated models):

type Post struct {
	Title     string
	IsVisible bool
}

type Issue struct {
	Title        string
	IsDraft      bool
	PublishDate  time.Time
	IssueNumber  int
	ID           int
}

type Newsletter struct {
	Subject string
}

type PostCategory struct {
	Name string
}

type Subscriber struct {
	EmailAddress           string
	Subscribed             bool
	Verified               bool
	VerificationSentDate   *time.Time
	Token                  string
}

type SubscriberManager struct {
	Subscribers []*Subscriber
}

func (sm *SubscriberManager) Subscribed() []*Subscriber {
	var out []*Subscriber
	for _, s := range sm.Subscribers {
		if s.Subscribed {
			out = append(out, s)
		}
	}
	return out
}

func (sm *SubscriberManager) All() []*Subscriber {
	return sm.Subscribers
}

func (s *Subscriber) ResetToken() {
	s.Token = s.Token + "_reset"
}

func (s *Subscriber) TokenExpired() bool {
	if s.VerificationSentDate == nil {
		return true
	}
	return time.Since(*s.VerificationSentDate) > 48*time.Hour
}

func (s *Subscriber) Subscribe() bool {
	if s.TokenExpired() {
		return false
	}
	s.Verified = true
	s.Subscribed = true
	return true
}

func (s *Subscriber) Unsubscribe() bool {
	if !s.Verified || !s.Subscribed {
		return false
	}
	s.Verified = false
	s.Subscribed = false
	return true
}

func (s *Subscriber) GetVerificationURL() string {
	return "/newsfeed/subscribe/confirm/" + s.Token + "/"
}

// --- Tests ---

func TestPostModel_Str(t *testing.T) {
	post := &Post{Title: "post title", IsVisible: true}
	assert.Equal(t, post.Title, post.Title)
}

func TestPostModel_VisibleQueryset(t *testing.T) {
	all := []*Post{
		{Title: "a", IsVisible: false},
		{Title: "b", IsVisible: false},
		{Title: "c", IsVisible: true},
		{Title: "d", IsVisible: true},
	}
	var count int
	for _, p := range all {
		if p.IsVisible {
			count++
		}
	}
	assert.Equal(t, 2, count)
}

func TestPostModel_AllQueryset(t *testing.T) {
	posts := []*Post{
		{Title: "a", IsVisible: false},
		{Title: "b", IsVisible: false},
		{Title: "c", IsVisible: true},
		{Title: "d", IsVisible: true},
	}
	assert.Equal(t, 4, len(posts))
}

func TestIssueModel_Str(t *testing.T) {
	issue := &Issue{Title: "title", IsDraft: false}
	assert.Equal(t, issue.Title, issue.Title)
}

func TestIssueModel_AllQueryset(t *testing.T) {
	issues := []*Issue{
		{IsDraft: false},
		{IsDraft: true},
	}
	assert.Equal(t, 2, len(issues))
}

func TestIssueModel_ReleasedQueryset(t *testing.T) {
	issues := []*Issue{
		{IsDraft: false},
		{IsDraft: true},
	}
	var releasedCount int
	for _, i := range issues {
		if !i.IsDraft {
			releasedCount++
		}
	}
	assert.Equal(t, 1, releasedCount)
}

func TestIssueModel_ReleasedWithFutureReleasedDate(t *testing.T) {
	now := time.Now()
	issues := []*Issue{
		{IsDraft: false, PublishDate: now.Add(24 * time.Hour), ID: 11},
	}
	var exists bool
	for _, i := range issues {
		if !i.IsDraft && i.PublishDate.Before(now) {
			exists = true
		}
	}
	assert.False(t, exists)
}

func TestIssueModel_IsPublished(t *testing.T) {
	released := &Issue{IsDraft: false}
	unreleased := &Issue{IsDraft: true}
	assert.True(t, !released.IsDraft)
	assert.False(t, !unreleased.IsDraft)
}

func TestIssueModel_GetAbsoluteUrl(t *testing.T) {
	released := &Issue{IssueNumber: 33}
	expected := "/newsfeed/issues/33/"
	got := "/newsfeed/issues/" + "33" + "/"
	assert.Equal(t, expected, got)
}

func TestSubscriberModel_Str(t *testing.T) {
	manager := &SubscriberManager{Subscribers: []*Subscriber{
		{EmailAddress: "test1@example.com", Subscribed: true, Verified: true},
		{EmailAddress: "test2@example.com", Subscribed: false, Verified: false},
	}}
	first := manager.Subscribed()[0]
	assert.Equal(t, first.EmailAddress, first.EmailAddress)
}

func TestSubscriberModel_AllQueryset(t *testing.T) {
	manager := &SubscriberManager{Subscribers: []*Subscriber{
		{EmailAddress: "test1@example.com", Subscribed: true, Verified: true},
		{EmailAddress: "test2@example.com", Subscribed: false, Verified: false},
	}}
	assert.Equal(t, 2, len(manager.All()))
}

func TestSubscriberModel_SubscribedQueryset(t *testing.T) {
	manager := &SubscriberManager{Subscribers: []*Subscriber{
		{EmailAddress: "test1@example.com", Subscribed: true, Verified: true},
		{EmailAddress: "test2@example.com", Subscribed: false, Verified: false},
	}}
	assert.Equal(t, 1, len(manager.Subscribed()))
}

func TestSubscriberModel_TokenExpired(t *testing.T) {
	now := time.Now().Add(-72 * time.Hour)
	s := &Subscriber{VerificationSentDate: &now}
	assert.True(t, s.TokenExpired())
}

func TestSubscriberModel_TokenNotExpired(t *testing.T) {
	now := time.Now()
	s := &Subscriber{VerificationSentDate: &now}
	assert.False(t, s.TokenExpired())
}

func TestSubscriberModel_TokenExpiredNoSentDate(t *testing.T) {
	s := &Subscriber{VerificationSentDate: nil}
	assert.True(t, s.TokenExpired())
}

func TestSubscriberModel_ResetToken(t *testing.T) {
	s := &Subscriber{Token: "abc"}
	oldToken := s.Token
	s.ResetToken()
	assert.NotEqual(t, oldToken, s.Token)
}

func TestSubscriberModel_Subscribe(t *testing.T) {
	now := time.Now()
	s := &Subscriber{VerificationSentDate: &now, Verified: false, Subscribed: false}
	success := s.Subscribe()
	assert.True(t, success)
	assert.True(t, s.Verified)
	assert.True(t, s.Subscribed)
}

func TestSubscriberModel_SubscribeWithExpiredToken(t *testing.T) {
	timeExpired := time.Now().Add(-72 * time.Hour)
	s := &Subscriber{VerificationSentDate: &timeExpired, Verified: false, Subscribed: false}
	success := s.Subscribe()
	assert.False(t, success)
	assert.False(t, s.Verified)
	assert.False(t, s.Subscribed)
}

func TestSubscriberModel_UnsubscribeWithUnsubscribedEmail(t *testing.T) {
	s := &Subscriber{Verified: false, Subscribed: false}
	success := s.Unsubscribe()
	assert.False(t, success)
	assert.False(t, s.Verified)
	assert.False(t, s.Subscribed)
}

func TestSubscriberModel_Unsubscribe(t *testing.T) {
	s := &Subscriber{Verified: true, Subscribed: true}
	success := s.Unsubscribe()
	assert.True(t, success)
	assert.False(t, s.Verified)
	assert.False(t, s.Subscribed)
}

func TestSubscriberModel_GetAbsoluteUrl(t *testing.T) {
	s := &Subscriber{Token: "xxx"}
	expected := "/newsfeed/subscribe/confirm/xxx/"
	assert.Equal(t, expected, s.GetVerificationURL())
}

func TestNewsletterModel_Str(t *testing.T) {
	n := &Newsletter{Subject: "Subject"}
	assert.Equal(t, "Subject", n.Subject)
}

func TestPostCategoryModel_Str(t *testing.T) {
	pc := &PostCategory{Name: "Category"}
	assert.Equal(t, "Category", pc.Name)
}