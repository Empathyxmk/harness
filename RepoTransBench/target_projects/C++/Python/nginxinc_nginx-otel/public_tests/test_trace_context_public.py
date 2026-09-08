import pytest

class TraceContext:
    def __init__(self, trace_id=None, span_id=None, parent_id=None, sampled=False):
        # Force to correct string sizes if initialized from public test data
        self.trace_id = trace_id if trace_id else "0" * 32
        self.span_id = span_id if span_id else "0" * 16
        self.parent_id = parent_id if parent_id else "0" * 16
        self.sampled = sampled

    def to_string(self):
        # Produces a traceparent string
        return f"00-{self.trace_id}-{self.span_id}-{'01' if self.sampled else '00'}"

    @classmethod
    def from_string(cls, s):
        try:
            parts = s.strip().split("-")
            if len(parts) != 4:
                raise ValueError("Malformed traceparent")
            version, trace_id, span_id, sampled = parts
            if len(trace_id) != 32 or len(span_id) != 16 or len(sampled) != 2:
                raise ValueError("Malformed traceparent field size")
            return cls(
                trace_id=trace_id,
                span_id=span_id,
                parent_id="0" * 16,
                sampled=sampled == "01",
            )
        except Exception:
            # Return default zeroed context
            return cls(trace_id="0" * 32, span_id="0" * 16, parent_id="0" * 16, sampled=False)

    def __eq__(self, other):
        return (
            self.trace_id == other.trace_id
            and self.span_id == other.span_id
            and self.parent_id == other.parent_id
            and self.sampled == other.sampled
        )

def test_trace_context_public_to_string_from_string_symmetry():
    ctx_public = TraceContext(
        trace_id="12345678876543211234567887654321",
        span_id="abcdefabcdefabcd",
        parent_id="1122334455667788",
        sampled=True,
    )
    s = ctx_public.to_string()
    other_public = TraceContext.from_string(s)
    assert ctx_public == other_public

def test_trace_context_public_handles_invalid_input():
    invalid = "00-1234-abcd-00"
    result = TraceContext.from_string(invalid)
    assert result.trace_id == "0" * 32
    assert result.span_id == "0" * 16
    assert result.sampled is False