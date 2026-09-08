package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestAdditionalClaimsAreIncluded(t *testing.T) {
	// Setup mock JWT app & injector
	app := NewTestJWTApp(map[string]interface{}{
		"JWT_SECRET_KEY": "addclaims_secret",
		"ADDITIONAL_CLAIMS": map[string]interface{}{"role": "editor", "active": false},
	})
	client := app.TestClient()

	token := app.CreateAccessToken("bbrown", nil)

	status, response := client.GetJSONWithAuth("/protected", token)
	assert.Equal(t, 200, status)
	assert.Equal(t, map[string]interface{}{"role": "editor", "active": false}, response)
}