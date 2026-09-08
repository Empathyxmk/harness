def import_proxy():
    from src.Structural.Proxy import add_to_image_cache, proxied_network_fetch
    return add_to_image_cache, proxied_network_fetch

def test_should_return_from_network():
    _, proxied_network_fetch = import_proxy()
    assert proxied_network_fetch('catPic.jpg') == 'catPic.jpg - Response from network'

def test_should_return_from_cache():
    _, proxied_network_fetch = import_proxy()
    assert proxied_network_fetch('dogPic.jpg') == 'dogPic.jpg - Response from network'
    assert proxied_network_fetch('dogPic.jpg') == 'dogPic.jpg - Response from cache'