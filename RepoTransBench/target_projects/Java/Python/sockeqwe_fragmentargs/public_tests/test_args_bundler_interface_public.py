from tests.original.test_args_bundler_interface import Bundle, ArgsBundler

class PublicTestBundler(ArgsBundler):
    def put(self, key, value, bundle):
        bundle[key] = f"PUBLIC_{value}_PUBTEST"

    def get(self, key, bundle):
        v = bundle.get(key)
        if v is None:
            return None
        return v.replace("PUBLIC_", "").replace("_PUBTEST", "")

def test_interface_put_adds_prefix_suffix_public():
    bundle = Bundle()
    PublicTestBundler().put("PUBKEY", "valueForPublic", bundle)
    assert bundle["PUBKEY"] == "PUBLIC_valueForPublic_PUBTEST"

def test_interface_get_removes_prefix_suffix_public():
    bundle = Bundle()
    bundle["PUB_KEY"] = "PUBLIC_zxy_PUBTEST"
    assert PublicTestBundler().get("PUB_KEY", bundle) == "zxy"