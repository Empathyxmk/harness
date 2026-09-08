package original

import (
    "reflect"
    "strings"
    "testing"
    "time"
    "github.com/stretchr/testify/assert"
    "owncloudpyocclient/owncloud"
)

// -------------- TestResponseError ---------------

func TestResponseErrorInitWithInt(t *testing.T) {
    err := owncloud.NewResponseError(404, "MyErr")
    assert.Equal(t, 404, err.StatusCode)
    assert.Equal(t, "MyErr error: 404", err.Error())
}

func TestResponseErrorInitWithResponse(t *testing.T) {
    fake := &owncloud.FakeResponse{
        StatusCode: 400,
        Content:    []byte("resbody"),
    }
    err := owncloud.NewResponseError(fake, "OCS")
    assert.Equal(t, 400, err.StatusCode)
    assert.Equal(t, []byte("resbody"), err.GetResourceBody())
    str := err.Error()
    assert.True(t, strings.HasPrefix(str, "HTTP error: 400 (OCS)"), str)
}

func TestResponseErrorInitWithResponseStrcontent(t *testing.T) {
    fake := &owncloud.FakeResponse{
        StatusCode: 501,
        Content:    "Some string",
    }
    err := owncloud.NewResponseError(fake, "Txt")
    assert.Equal(t, 501, err.StatusCode)
    assert.Equal(t, "Some string", err.GetResourceBody())
    str := err.Error()
    assert.True(t, strings.Contains(str, "Some string"), str)
}

func TestResponseErrorReprAndBranching(t *testing.T) {
    rr := owncloud.NewResponseError(401)
    assert.Equal(t, "HTTP error: 401", rr.Error())
    // no content property
    fake := &owncloud.FakeResponse{
        StatusCode: 500,
    }
    err2 := owncloud.NewResponseError(fake)
    assert.Nil(t, err2.GetResourceBody())
    assert.True(t, strings.Contains(err2.Error(), "HTTP error: 500"))
}

// -------------- TestOCSResponseError ------------

func TestOCSResponseErrorXMLMsg(t *testing.T) {
    fake := &owncloud.FakeResponse{
        StatusCode: 500,
        Content:    []byte(`<root><message>failmsg</message></root>`),
    }
    err := owncloud.NewOCSResponseError(fake)
    assert.True(t, strings.Contains(err.Error(), "failmsg"))
    assert.Equal(t, []byte(`<root><message>failmsg</message></root>`), err.GetResourceBody())
}

func TestOCSResponseErrorXMLInvalid(t *testing.T) {
    fake := &owncloud.FakeResponse{
        StatusCode: 400,
        Content:    []byte(`not<xml`),
    }
    err := owncloud.NewOCSResponseError(fake)
    assert.True(t, strings.Contains(err.Error(), "OCS response error"))
    assert.Equal(t, []byte(`not<xml`), err.GetResourceBody())
}

func TestOCSResponseErrorNone(t *testing.T) {
    fake := &owncloud.FakeResponse{}
    err := owncloud.NewOCSResponseError(fake)
    assert.Nil(t, err.GetResourceBody())
}

// -------------- TestShareInfo -------------------

func TestShareInfoGetters(t *testing.T) {
    info := map[string]interface{}{
        "id": "123",
        "share_type": "1",
        "permissions": "3",
        "share_with": "user1",
        "share_with_displayname": "User One",
        "stime": "1777777700",
        "expiration": "2024-12-31",
        "path": "/some.txt",
    }
    s := owncloud.NewShareInfo(info)
    assert.Equal(t, 123, s._getInt("id"))
    assert.Equal(t, 1, s._getInt("share_type"))
    assert.Equal(t, "user1", s.getShareWith())
    assert.Equal(t, "User One", s.getShareWithDisplayName())
    assert.Equal(t, "/some.txt", s.getPath())
    assert.Equal(t, "2024-12-31", s.getExpiration())
    shareTime := s.getShareTime()
    _, ok := shareTime.(time.Time)
    assert.True(t, ok)
}

func TestShareInfoIntConversion(t *testing.T) {
    info := map[string]interface{}{
        "id": 123,
        "permissions": "",
        "share_type": nil,
        "stime": "1777777700",
        "expiration": nil,
    }
    s := owncloud.NewShareInfo(info)
    assert.Equal(t, 123, s._getInt("id"))
    assert.Nil(t, s._getInt("permissions"))
    assert.Nil(t, s._getInt("share_type"))
    shareTime := s.getShareTime()
    _, ok := shareTime.(time.Time)
    assert.True(t, ok)
}

func TestShareInfoMissingAttrs(t *testing.T) {
    s := owncloud.NewShareInfo(map[string]interface{}{})
    assert.Nil(t, s.getShareWith())
    assert.Nil(t, s.getShareWithDisplayName())
    assert.Nil(t, s.getPath())
}

func TestShareInfoDelAttrsRemoved(t *testing.T) {
    info := map[string]interface{}{
        "id": "1",
        "storage": "xxx",
        "mail_send": 1,
        "item_type": "foo",
        "item_source": 42,
        "file_source": 15,
        "parent": nil,
        "other": "ok",
        "stime": "1000",
    }
    s := owncloud.NewShareInfo(info)
    s.delAttrs()
    _, itemType := s.ShareInfo["item_type"]
    _, parent := s.ShareInfo["parent"]
    _, id := s.ShareInfo["id"]
    assert.False(t, itemType)
    assert.False(t, parent)
    assert.True(t, id)
}

func TestShareInfoContainsAndGetitem(t *testing.T) {
    m := map[string]interface{}{
        "id": 99,
        "foo": "bar",
    }
    s := owncloud.NewShareInfo(m)
    assert.True(t, s.Has("id"))
    assert.Equal(t, "bar", s.Get("foo"))
}

// ----------------- TestUtils -------------------

func TestUtilsEscapeUnescape(t *testing.T) {
    p := "/a b/abc.txt"
    out := owncloud.EscapePath(p)
    assert.True(t, strings.Contains(out, "%20"))
    assert.Equal(t, owncloud.UnescapePath(out), p)
}

func TestUtilsToUnicodeBytes(t *testing.T) {
    assert.Equal(t, "abc", owncloud.ToUnicode([]byte("abc")))
    assert.Equal(t, "xyz", owncloud.ToUnicode("xyz"))
}

func TestUtilsToBytes(t *testing.T) {
    assert.Equal(t, []byte("xyz"), owncloud.ToBytes("xyz"))
    assert.Equal(t, []byte("xyz"), owncloud.ToBytes([]byte("xyz")))
}

func TestUtilsStripTrailingSlash(t *testing.T) {
    assert.Equal(t, "foo", *owncloud.StripTrailingSlash("foo/"))
    assert.Equal(t, "/bar", *owncloud.StripTrailingSlash("/bar/"))
    assert.Equal(t, "/", *owncloud.StripTrailingSlash("/"))
    assert.Nil(t, owncloud.StripTrailingSlash(""))
}