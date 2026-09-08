import sys

def test_cpp_version_equivalent(monkeypatch):
    # C++ version macro; in python we use sys.version_info
    import platform
    cpp_ver_sim = "N/A"
    gcc_ver = "N/A"
    libstdcpp_ver = "unknown version,please check or config your gcc path,or your OS not surpport."
    # In C++; __cplusplus, __VERSION__, __GNUC__, __GNUC_MINOR__, __GNUC_PATCHLEVEL__, __GLIBCXX__
    # In python just check the interpreter
    print("python version = {}".format(platform.python_version()))
    print("sys.version = {}".format(sys.version))
    print("python major = {}".format(sys.version_info.major))
    print("python minor = {}".format(sys.version_info.minor))
    print("python patch = {}".format(sys.version_info.micro))
    print("libstdc++ = {}".format(libstdcpp_ver))
    # Always passes; just information as in main()
    assert True