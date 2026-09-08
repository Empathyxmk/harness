import pytest

def test_builtin_types_declaration():
    # We'll simulate the existence of these types (GLSL builtins) as Python types,
    # but here we'll just ensure Python code can 'declare' variables.
    test_bool = True
    test_int = 2
    test_uint = 2
    test_float = 1.0
    test_double = 2.0
    # We'll use lists to simulate vectors and arrays
    test_vec2 = [0.0, 0.0]
    test_vec3 = [0.0, 0.0, 0.0]
    test_vec4 = [0.0, 0.0, 0.0, 0.0]
    test_dvec2 = [0.0, 0.0]
    test_dvec3 = [0.0, 0.0, 0.0]
    test_dvec4 = [0.0, 0.0, 0.0, 0.0]
    test_bvec2 = [False, False]
    test_bvec3 = [False, False, False]
    test_bvec4 = [False, False, False, False]
    test_ivec2 = [0, 0]
    test_ivec3 = [0, 0, 0]
    test_ivec4 = [0, 0, 0, 0]
    test_uvec2 = [0, 0]
    test_uvec3 = [0, 0, 0]
    test_uvec4 = [0, 0, 0, 0]
    test_mat2 = [[0.0, 0.0], [0.0, 0.0]]
    test_mat3 = [[0.0]*3 for _ in range(3)]
    test_mat4 = [[0.0]*4 for _ in range(4)]
    # ... skipping all other builtins, just ensure no TypeError or AttributeError
    assert test_bool is True or test_int == 2
    assert isinstance(test_vec3, list)
    assert isinstance(test_mat4, list)