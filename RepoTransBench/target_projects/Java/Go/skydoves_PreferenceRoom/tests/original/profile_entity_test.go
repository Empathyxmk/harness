package original

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

type PrivateInfo struct {
	Name string
	Age  int
}
type Pet struct {
	Name  string
	Age   int
	Feed  bool
	Color int
}

// Simulated Profile Entity
type UserProfile struct {
	Nickname string
	Login    bool
	Visits   int
	UserInfo *PrivateInfo
	UserPet  *Pet
	Preferences map[string]interface{}
}

func NewUserProfile() *UserProfile {
	return &UserProfile{
		Nickname: "skydoves!!!",
		Login:    false,
		Visits:   1,
		UserInfo: &PrivateInfo{Name: "null", Age: 0},
		UserPet:  nil,
		Preferences: make(map[string]interface{}),
	}
}
func (u *UserProfile) clear() { *u = *NewUserProfile() }
func (u *UserProfile) getkeyNameList() []string { return []string{"nickname", "Login", "visits", "userinfo", "userPet"} }
func (u *UserProfile) getNickname() string {
	if val, ok := u.Preferences["nickname"]; ok {
		return "Hello, " + val.(string) + "!!!"
	}
	return u.Nickname
}
func (u *UserProfile) getLogin() bool {
	if val, ok := u.Preferences["Login"]; ok {
		return val.(bool)
	}
	return u.Login
}
func (u *UserProfile) getVisits() int {
	if val, ok := u.Preferences["visits"]; ok {
		return val.(int) + 1
	}
	return u.Visits
}
func (u *UserProfile) getUserinfo() *PrivateInfo {
	if val, ok := u.Preferences["userinfo"]; ok {
		return val.(*PrivateInfo)
	}
	return u.UserInfo
}
func (u *UserProfile) getUserPet() *Pet {
	if val, ok := u.Preferences["userPet"]; ok {
		return val.(*Pet)
	}
	return u.UserPet
}
func (u *UserProfile) putNickname(s string) {
	u.Preferences["nickname"] = s
}
func (u *UserProfile) putLogin(v bool) { u.Preferences["Login"] = v }
func (u *UserProfile) putVisits(v int) { u.Preferences["visits"] = v }
func (u *UserProfile) putUserinfo(pi *PrivateInfo) { u.Preferences["userinfo"] = pi }
func (u *UserProfile) putUserPet(p *Pet)           { u.Preferences["userPet"] = p }
func (u *UserProfile) nicknameKeyName() string     { return "nickname" }
func (u *UserProfile) LoginKeyName() string        { return "Login" }
func (u *UserProfile) visitsKeyName() string       { return "visits" }
func (u *UserProfile) userPetKeyName() string      { return "userPet" }

func TestPreference(t *testing.T) {
	profile := NewUserProfile()
	profile.clear()
	profile.Preferences[profile.nicknameKeyName()] = "PreferenceRoom"
	profile.Preferences[profile.LoginKeyName()] = true
	profile.Preferences[profile.visitsKeyName()] = 12

	assert.Equal(t, "Hello, PreferenceRoom!!!", profile.getNickname())
	assert.Equal(t, true, profile.getLogin())
	assert.Equal(t, 13, profile.getVisits())
}

func TestDefault(t *testing.T) {
	profile := NewUserProfile()
	profile.clear()
	assert.Equal(t, "skydoves!!!", profile.getNickname())
	assert.Equal(t, false, profile.getLogin())
	assert.Equal(t, 1, profile.getVisits())
	assert.Equal(t, "null", profile.getUserinfo().Name)
	assert.Nil(t, profile.getUserPet())
}

func TestPutPreference(t *testing.T) {
	profile := NewUserProfile()
	profile.clear()
	profile.putNickname("PreferenceRoom")
	profile.putLogin(true)
	profile.putVisits(12)
	profile.putUserinfo(&PrivateInfo{Name: "Jaewoong", Age: 123})

	assert.Equal(t, "Hello, PreferenceRoom!!!", profile.getNickname())
	assert.Equal(t, true, profile.getLogin())
	assert.Equal(t, 13, profile.getVisits())
	assert.Equal(t, "Jaewoong", profile.getUserinfo().Name)
	assert.Equal(t, 123, profile.getUserinfo().Age)
}

func TestBaseGsonConverter(t *testing.T) {
	profile := NewUserProfile()
	profile.clear()
	pet := &Pet{Name: "skydoves", Age: 11, Feed: true, Color: 0xFFFFFFFF}
	profile.putUserPet(pet)

	assert.NotNil(t, profile.Preferences[profile.userPetKeyName()])
	petFromPref := profile.getUserPet()
	assert.Equal(t, "skydoves", petFromPref.Name)
	assert.Equal(t, 11, petFromPref.Age)
	assert.Equal(t, true, petFromPref.Feed)
	assert.Equal(t, 0xFFFFFFFF, petFromPref.Color)
}

func TestKeyNameList(t *testing.T) {
	profile := NewUserProfile()
	assert.Equal(t, 5, len(profile.getkeyNameList()))
}