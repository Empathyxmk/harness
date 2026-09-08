from collections import namedtuple
import niquests
import pytest
import socket
import time
import urllib3

# Public variant: Use different port numbers, paths, headers, status codes

NGINX_CONFIG = """
{{ globals }}

daemon off;

events {
}

http {
    {{ http_globals }}

    ssl_certificate localhost.crt;
    ssl_certificate_key localhost.key;

    otel_exporter {
        endpoint {{ endpoint or "127.0.0.1:14327" }};  # Public: different port
        interval {{ interval or "2ms" }};
        batch_size 4;
        batch_count 2;

        {{ exporter_opts }}
    }

    otel_trace on;
    {{ resource_attrs }}

    server {
        listen       127.0.0.1:19443 ssl;
        listen       127.0.0.1:19443 quic;
        listen       127.0.0.1:19090;

        http2 on;

        server_name  localhost2;

        location /healthy {
            return 200 "HEALTHY";
        }

        location /fail {
            return 400 "FAIL";
        }

        location /publiccustom {
            otel_span_name my_public_location;
            otel_span_attr http.public.completion
                $request_completion;
            otel_span_attr http.response.header.content.type
                $sent_http_content_type;
            otel_span_attr http.request $request;
            return 200 "HEALTHY";
        }

        location /vars_public {
            otel_trace_context extract;
            add_header "X-Otel-Trace-Id" $otel_trace_id;
            add_header "X-Otel-Span-Id" $otel_span_id;
            add_header "X-Otel-Parent-Id" $otel_parent_id;
            add_header "X-Otel-Parent-Sampled" $otel_parent_sampled;
            return 205;
        }

        location /ignore_public {
            proxy_pass http://127.0.0.1:19090/notrace_public;
        }

        location /extract_public {
            otel_trace_context extract;
            proxy_pass http://127.0.0.1:19090/notrace_public;
        }

        location /inject_public {
            otel_trace_context inject;
            proxy_pass http://127.0.0.1:19090/notrace_public;
        }

        location /propagate_public {
            otel_trace_context propagate;
            proxy_pass http://127.0.0.1:19090/notrace_public;
        }

        location /notrace_public {
            otel_trace off;
            add_header "X-Otel-Traceparent" $http_traceparent;
            add_header "X-Otel-Tracestate" $http_tracestate;
            return 205;
        }
    }
}

"""

TraceContext = namedtuple("TraceContext", ["trace_id", "span_id", "state"])

# Public: New trace id, span id, state strings
parent_ctx = TraceContext(
    trace_id="1bf8651957ce43ee9558db322d90429c",
    span_id="aabbccddeeff1122",
    state="public=abcXYZ,example=112233445566",
)

def trace_headers(ctx):
    return (
        {
            "Traceparent": f"00-{ctx.trace_id}-{ctx.span_id}-01",
            "Tracestate": ctx.state,
        }
        if ctx
        else {"Traceparent": None, "Tracestate": None}
    )

def get_attr(span, name):
    for value in (a.value for a in span.attributes if a.key == name):
        return getattr(value, value.WhichOneof("value"))

@pytest.fixture
def client(nginx):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    with niquests.Session(multiplexed=True) as s:
        yield s

def test_http09_public(trace_service, nginx):

    def get_http09(host, port, path):
        with socket.create_connection((host, port)) as sock:
            sock.sendall(f"GET {path}\n".encode())
            resp = sock.recv(1024).decode("utf-8")
        return resp

    assert get_http09("127.0.0.1", 19090, "/healthy") == "HEALTHY"

    span = trace_service.get_span()
    assert span.name == "/healthy"

@pytest.mark.parametrize("http_ver", ["1.0", "2.0", "3.0"])
@pytest.mark.parametrize(
    ("path", "status"),
    [("/healthy", 200), ("/fail", 400)],
)
def test_default_attributes_public(client, trace_service, http_ver, path, status):
    # Port and scheme changed from original private test
    scheme, port = ("http", 19090) if http_ver == "1.0" else ("https", 19443)
    if http_ver == "3.0":
        client.quic_cache_layer.add_domain("127.0.0.1", port)
    r = client.get(f"{scheme}://127.0.0.1:{port}{path}", verify=False)

    span = trace_service.get_span()
    assert span.name == path
    assert get_attr(span, "http.method") == "GET"
    assert get_attr(span, "http.target") == path
    assert get_attr(span, "http.route") == path
    assert get_attr(span, "http.scheme") == scheme
    assert get_attr(span, "http.flavor") == http_ver
    assert get_attr(span, "http.user_agent") == (
        f"niquests/{niquests.__version__}"
    )
    assert get_attr(span, "http.request_content_length") == 0
    assert get_attr(span, "http.response_content_length") == len(r.text)
    assert get_attr(span, "http.status_code") == status
    assert get_attr(span, "net.host.name") == "localhost2"
    assert get_attr(span, "net.host.port") == port
    assert get_attr(span, "net.sock.peer.addr") == "127.0.0.1"
    assert get_attr(span, "net.sock.peer.port") in range(1024, 65536)

def test_custom_attributes_public(client, trace_service):
    assert client.get("http://127.0.0.1:19090/publiccustom").status_code == 200

    span = trace_service.get_span()
    assert span.name == "my_public_location"

    assert get_attr(span, "http.public.completion") == "HEALTHY"
    value = get_attr(span, "http.response.header.content.type")
    assert value.values[0].string_value == "text/plain"
    assert get_attr(span, "http.request") == "GET /publiccustom HTTP/1.1"

def test_trace_off_public(client, trace_service):
    assert client.get("http://127.0.0.1:19090/notrace_public").status_code == 205

    time.sleep(0.01)
    assert len(trace_service.batches) == 0

@pytest.mark.parametrize("parent", [None, parent_ctx])
def test_variables_public(client, trace_service, parent):
    r = client.get("http://127.0.0.1:19090/vars_public", headers=trace_headers(parent))

    span = trace_service.get_span()
    if parent:
        assert span.trace_id.hex() == parent.trace_id
        assert span.parent_span_id.hex() == parent.span_id
    else:
        assert span.parent_span_id == b"\x00"*8
    # headers changed from private test
    assert r.headers["X-Otel-Trace-Id"] == span.trace_id.hex()
    assert r.headers["X-Otel-Span-Id"] == span.span_id.hex()
    assert r.headers["X-Otel-Parent-Id"] == span.parent_span_id.hex()
    assert "X-Otel-Parent-Sampled" in r.headers