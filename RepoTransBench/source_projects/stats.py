#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版项目复杂度统计脚本
统计 #Tokens #Lines #Funcs #Classes #Imports 以及文件内依赖和跨文件依赖数量
支持特殊项目的特殊处理
"""

import os
import re
import json
import statistics
from pathlib import Path
from collections import defaultdict, Counter
import tiktoken
from typing import Dict, List, Set, Tuple, Any

class EnhancedProjectComplexityAnalyzer:
    def __init__(self, base_path: str = "./"):
        self.base_path = Path(base_path)
        self.encoding = tiktoken.get_encoding("cl100k_base")  # GPT-4 tokenizer
        
        # 定义特殊项目的处理规则
        self.special_projects = {
            'danmar_simplecpp': {
                'language': 'C',
                'additional_extensions': ['.cpp', '.cc', '.cxx', '.hpp', '.hxx', '.h++'],
                'ignore_overrides': {}
            },
            'brettlangdon_jsnice': {
                'language': 'JavaScript',
                'additional_extensions': [],
                'ignore_overrides': {
                    'exclude_dirs': ['lib']  # 不排除lib目录
                }
            }
        }
        
        # 定义需要忽略的目录和文件模式
        self.ignore_patterns = {
            'JavaScript': {
                'dirs': [
                    'node_modules', 'dist', 'build', 'coverage', '.next', '.nuxt',
                    'public', 'static', 'assets', 'out', 'tmp', 'temp', '.cache',
                    'bower_components', 'jspm_packages', '.npm', '.yarn',
                    'vendor', 'lib', 'libs', 'bundle', 'bundles', 'min',
                    '.git', '.vscode', '.idea', '__pycache__', 'logs', 'coverage'
                ],
                'files': [
                    '*.min.js', '*.min.css', '*.map', '*.lock', '*.log',
                    'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
                    '*.bundle.js', '*.chunk.js', '*.d.ts'
                ]
            },
            'Python': {
                'dirs': [
                    '__pycache__', '.pytest_cache', '.mypy_cache', '.tox',
                    'venv', 'env', '.venv', '.env', 'site-packages',
                    'build', 'dist', '.git', '.vscode', '.idea', 'logs'
                ],
                'files': ['*.pyc', '*.pyo', '*.pyd', '*.log', '*.egg-info']
            },
            'Java': {
                'dirs': [
                    'target', 'build', 'out', '.gradle', '.mvn', 'bin',
                    '.git', '.vscode', '.idea', 'logs', 'lib', 'libs'
                ],
                'files': ['*.class', '*.jar', '*.war', '*.ear', '*.log']
            },
            'C#': {
                'dirs': [
                    'bin', 'obj', 'packages', '.vs', 'Debug', 'Release',
                    '.git', '.vscode', '.idea', 'logs', 'lib', 'libs'
                ],
                'files': ['*.dll', '*.exe', '*.pdb', '*.cache', '*.log']
            },
            'C': {
                'dirs': [
                    'build', 'cmake-build-debug', 'cmake-build-release',
                    '.git', '.vscode', '.idea', 'logs', 'lib', 'libs'
                ],
                'files': ['*.o', '*.obj', '*.exe', '*.out', '*.log', '*.so', '*.dll']
            },
            'C++': {
                'dirs': [
                    'build', 'cmake-build-debug', 'cmake-build-release',
                    '.git', '.vscode', '.idea', 'logs', 'lib', 'libs'
                ],
                'files': ['*.o', '*.obj', '*.exe', '*.out', '*.log', '*.so', '*.dll']
            },
            'Matlab': {
                'dirs': [
                    '.git', '.vscode', '.idea', 'logs', 'lib', 'libs'
                ],
                'files': ['*.log', '*.asv']
            }
        }
        
        # 定义文件大小限制（字节）
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        
        # 定义各语言的文件扩展名
        self.language_extensions = {
            'C': ['.c', '.h'],
            'C++': ['.cpp', '.cc', '.cxx', '.hpp', '.hxx', '.h++'],
            'JavaScript': ['.js', '.jsx', '.ts', '.tsx', '.mjs'],
            'Python': ['.py', '.pyx', '.pyi'],
            'C#': ['.cs'],
            'Java': ['.java'],
            'Matlab': ['.m', '.mlx']
        }
        
        # 定义各语言的函数定义模式
        self.function_patterns = {
            'C': [
                r'\b(?:static\s+)?(?:inline\s+)?(?:extern\s+)?(?:const\s+)?(?:unsigned\s+)?(?:signed\s+)?(?:long\s+)?(?:short\s+)?(?:int|char|float|double|void|bool)\s*\*?\s*\**\s*(\w+)\s*\([^)]*\)\s*{',
                r'\b(?:typedef\s+)?(?:struct|union|enum)\s+\w+\s*{',
            ],
            'C++': [
                r'\b(?:static\s+)?(?:inline\s+)?(?:extern\s+)?(?:const\s+)?(?:virtual\s+)?(?:unsigned\s+)?(?:signed\s+)?(?:long\s+)?(?:short\s+)?(?:int|char|float|double|void|bool|string|auto)\s*\*?\s*\**\s*(\w+)\s*\([^)]*\)\s*(?:const\s+)?{',
                r'\b(?:template\s*<[^>]*>\s*)?(?:class|struct)\s+(\w+)',
                r'\b(\w+)::\w+\s*\([^)]*\)\s*{',
            ],
            'JavaScript': [
                r'\bfunction\s+(\w+)\s*\([^)]*\)\s*{',
                r'\b(\w+)\s*:\s*function\s*\([^)]*\)\s*{',
                r'\b(\w+)\s*=\s*function\s*\([^)]*\)\s*{',
                r'\b(\w+)\s*=\s*\([^)]*\)\s*=>\s*{',
                r'\b(\w+)\s*=\s*async\s*\([^)]*\)\s*=>\s*{',
                r'\basync\s+function\s+(\w+)\s*\([^)]*\)\s*{',
                r'\b(\w+)\s*\([^)]*\)\s*{',  # 方法定义
            ],
            'Python': [
                r'\bdef\s+(\w+)\s*\([^)]*\):',
                r'\basync\s+def\s+(\w+)\s*\([^)]*\):',
            ],
            'C#': [
                r'\b(?:public|private|protected|internal)\s+(?:static\s+)?(?:virtual\s+)?(?:override\s+)?(?:abstract\s+)?(?:async\s+)?(?:void|int|string|bool|double|float|char|long|short|byte|object|var|[\w\[\]<>]+)\s+(\w+)\s*\([^)]*\)\s*{',
                r'\b(?:public|private|protected|internal)\s+(\w+)\s*\([^)]*\)\s*{',  # 构造函数
            ],
            'Java': [
                r'\b(?:public|private|protected)\s+(?:static\s+)?(?:final\s+)?(?:abstract\s+)?(?:synchronized\s+)?(?:void|int|String|boolean|double|float|char|long|short|byte|Object|[\w\[\]<>]+)\s+(\w+)\s*\([^)]*\)\s*{',
                r'\b(?:public|private|protected)\s+(\w+)\s*\([^)]*\)\s*{',  # 构造函数
            ],
            'Matlab': [
                r'\bfunction\s+(?:\[?[\w,\s]*\]?\s*=\s*)?(\w+)\s*\([^)]*\)',
            ]
        }
        
        # 定义各语言的类定义模式
        self.class_patterns = {
            'C': [
                r'\btypedef\s+struct\s+(\w+)',
                r'\bstruct\s+(\w+)\s*{',
                r'\bunion\s+(\w+)\s*{',
                r'\benum\s+(\w+)\s*{',
            ],
            'C++': [
                r'\bclass\s+(\w+)(?:\s*:\s*(?:public|private|protected)\s+[\w:]+)?',
                r'\bstruct\s+(\w+)(?:\s*:\s*(?:public|private|protected)\s+[\w:]+)?',
                r'\bunion\s+(\w+)',
                r'\benum\s+(?:class\s+)?(\w+)',
                r'\btemplate\s*<[^>]*>\s*(?:class|struct)\s+(\w+)',
            ],
            'JavaScript': [
                r'\bclass\s+(\w+)(?:\s+extends\s+\w+)?',
                r'\bfunction\s+(\w+)\s*\([^)]*\)\s*{[^}]*this\.',  # 构造函数模式
                r'\b(\w+)\.prototype\s*=',
            ],
            'Python': [
                r'\bclass\s+(\w+)(?:\([^)]*\))?:',
            ],
            'C#': [
                r'\b(?:public|private|protected|internal)\s+(?:static\s+)?(?:abstract\s+)?(?:sealed\s+)?(?:partial\s+)?(?:class|struct|interface|enum)\s+(\w+)(?:\s*:\s*[\w\s,<>]+)?',
            ],
            'Java': [
                r'\b(?:public|private|protected)\s+(?:static\s+)?(?:final\s+)?(?:abstract\s+)?(?:class|interface|enum)\s+(\w+)(?:\s+extends\s+\w+)?(?:\s+implements\s+[\w\s,]+)?',
            ],
            'Matlab': [
                r'\bclassdef\s+(\w+)(?:\s*<\s*[\w\s&.]+)?',
            ]
        }
        
        # 定义各语言的导入模式
        self.import_patterns = {
            'C': [
                r'#include\s*[<"](.*?)[>"]',
            ],
            'C++': [
                r'#include\s*[<"](.*?)[>"]',
                r'using\s+namespace\s+(\w+)',
                r'using\s+(\w+::\w+)',
            ],
            'JavaScript': [
                r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]',
                r'import\s+[\'"]([^\'"]+)[\'"]',
                r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)',
                r'import\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)',
                r'export\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]',
            ],
            'Python': [
                r'import\s+([\w\.]+)(?:\s+as\s+\w+)?',
                r'from\s+([\w\.]+)\s+import\s+.*',
            ],
            'C#': [
                r'using\s+([\w\.]+);',
                r'using\s+static\s+([\w\.]+);',
            ],
            'Java': [
                r'import\s+([\w\.]+);',
                r'import\s+static\s+([\w\.]+);',
            ],
            'Matlab': [
                r'import\s+([\w\.]+)',
                r'addpath\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)',
            ]
        }
        
        # 定义注释模式
        self.comment_patterns = {
            'C': [r'//.*?$', r'/\*.*?\*/'],
            'C++': [r'//.*?$', r'/\*.*?\*/'],
            'JavaScript': [r'//.*?$', r'/\*.*?\*/', r'^\s*\*.*?$'],
            'Python': [r'#.*?$', r'""".*?"""', r"'''.*?'''"],
            'C#': [r'//.*?$', r'/\*.*?\*/', r'///.*?$'],
            'Java': [r'//.*?$', r'/\*.*?\*/', r'/\*\*.*?\*/'],
            'Matlab': [r'%.*?$', r'%{.*?%}']
        }

    def get_project_extensions(self, project_path: Path, language: str) -> List[str]:
        """获取项目应该分析的文件扩展名"""
        project_name = project_path.name
        base_extensions = self.language_extensions.get(language, [])
        
        # 检查是否为特殊项目
        if project_name in self.special_projects:
            special_config = self.special_projects[project_name]
            if special_config['language'] == language:
                additional_extensions = special_config.get('additional_extensions', [])
                return base_extensions + additional_extensions
        
        return base_extensions

    def get_ignore_patterns_for_project(self, project_path: Path, language: str) -> Dict[str, List[str]]:
        """获取项目的忽略模式"""
        project_name = project_path.name
        base_patterns = self.ignore_patterns.get(language, {'dirs': [], 'files': []})
        
        # 检查是否为特殊项目
        if project_name in self.special_projects:
            special_config = self.special_projects[project_name]
            if special_config['language'] == language:
                ignore_overrides = special_config.get('ignore_overrides', {})
                
                # 创建修改后的忽略模式
                modified_patterns = {
                    'dirs': base_patterns['dirs'][:],  # 复制列表
                    'files': base_patterns['files'][:]  # 复制列表
                }
                
                # 处理排除某些目录的情况
                if 'exclude_dirs' in ignore_overrides:
                    for dir_to_exclude in ignore_overrides['exclude_dirs']:
                        if dir_to_exclude in modified_patterns['dirs']:
                            modified_patterns['dirs'].remove(dir_to_exclude)
                            print(f"特殊项目 {project_name}: 不忽略目录 '{dir_to_exclude}'")
                
                # 处理排除某些文件的情况
                if 'exclude_files' in ignore_overrides:
                    for file_to_exclude in ignore_overrides['exclude_files']:
                        if file_to_exclude in modified_patterns['files']:
                            modified_patterns['files'].remove(file_to_exclude)
                            print(f"特殊项目 {project_name}: 不忽略文件模式 '{file_to_exclude}'")
                
                return modified_patterns
        
        return base_patterns

    def should_ignore_path(self, path: Path, language: str, project_path: Path) -> bool:
        """检查路径是否应该被忽略"""
        ignore_patterns = self.get_ignore_patterns_for_project(project_path, language)
        
        # 检查是否在忽略的目录中
        for part in path.parts:
            if part in ignore_patterns['dirs']:
                return True
        
        # 检查文件名是否匹配忽略模式
        import fnmatch
        for pattern in ignore_patterns['files']:
            if fnmatch.fnmatch(path.name, pattern):
                return True
        
        return False

    def should_ignore_file(self, file_path: Path, language: str, project_path: Path) -> bool:
        """检查文件是否应该被忽略"""
        # 检查路径
        if self.should_ignore_path(file_path, language, project_path):
            return True
        
        # 检查文件大小
        try:
            if file_path.stat().st_size > self.max_file_size:
                print(f"忽略大文件: {file_path} ({file_path.stat().st_size / 1024 / 1024:.1f}MB)")
                return True
        except:
            return True
        
        return False

    def count_tokens(self, text: str) -> int:
        """使用tiktoken计算token数量"""
        try:
            tokens = self.encoding.encode(text)
            return len(tokens)
        except Exception as e:
            print(f"Token计算错误: {e}")
            return 0

    def count_lines(self, content: str) -> int:
        """统计代码行数（非空行）"""
        lines = content.split('\n')
        non_empty_lines = sum(1 for line in lines if line.strip())
        return non_empty_lines

    def remove_comments(self, content: str, language: str) -> str:
        """移除注释"""
        if language not in self.comment_patterns:
            return content
            
        for pattern in self.comment_patterns[language]:
            if pattern.endswith('$'):
                # 单行注释
                content = re.sub(pattern, '', content, flags=re.MULTILINE)
            else:
                # 多行注释
                content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)
        
        return content

    def count_functions(self, content: str, language: str) -> int:
        """统计函数数量"""
        if language not in self.function_patterns:
            return 0
        
        # 先移除注释
        clean_content = self.remove_comments(content, language)
        
        function_count = 0
        for pattern in self.function_patterns[language]:
            matches = re.findall(pattern, clean_content, re.MULTILINE)
            function_count += len(matches)
        
        return function_count

    def count_classes(self, content: str, language: str) -> int:
        """统计类数量"""
        if language not in self.class_patterns:
            return 0
        
        # 先移除注释
        clean_content = self.remove_comments(content, language)
        
        class_count = 0
        for pattern in self.class_patterns[language]:
            matches = re.findall(pattern, clean_content, re.MULTILINE)
            class_count += len(matches)
        
        return class_count

    def extract_imports(self, content: str, language: str) -> Tuple[Set[str], Set[str], Set[str]]:
        """提取导入语句，返回 (所有导入, 标准库导入, 跨文件导入)"""
        if language not in self.import_patterns:
            return set(), set(), set()
        
        # 先移除注释
        clean_content = self.remove_comments(content, language)
        
        all_imports = set()
        standard_imports = set()
        cross_file_imports = set()
        
        for pattern in self.import_patterns[language]:
            matches = re.findall(pattern, clean_content, re.MULTILINE)
            all_imports.update(matches)
            
            # 分类导入
            for match in matches:
                if self.is_standard_import(match, language):
                    standard_imports.add(match)
                elif self.is_cross_file_import(match, language):
                    cross_file_imports.add(match)
        
        return all_imports, standard_imports, cross_file_imports

    def is_standard_import(self, import_name: str, language: str) -> bool:
        """判断是否为标准库导入"""
        if language in ['C', 'C++']:
            # 标准库头文件
            standard_headers = {
                'stdio.h', 'stdlib.h', 'string.h', 'math.h', 'time.h', 'ctype.h',
                'assert.h', 'errno.h', 'float.h', 'limits.h', 'locale.h', 'setjmp.h',
                'signal.h', 'stdarg.h', 'stddef.h', 'wchar.h', 'wctype.h',
                # C++ 标准库
                'iostream', 'vector', 'string', 'algorithm', 'map', 'set', 'list',
                'deque', 'queue', 'stack', 'memory', 'thread', 'mutex', 'future',
                'chrono', 'random', 'regex', 'fstream', 'sstream', 'iomanip'
            }
            return import_name in standard_headers or import_name.startswith('std')
        
        elif language == 'JavaScript':
            # Node.js 内置模块
            builtin_modules = {
                'fs', 'path', 'os', 'crypto', 'http', 'https', 'url', 'querystring',
                'util', 'events', 'stream', 'buffer', 'child_process', 'cluster',
                'dgram', 'dns', 'net', 'tls', 'zlib', 'readline', 'repl', 'vm'
            }
            return import_name in builtin_modules
        
        elif language == 'Python':
            # Python 标准库模块
            standard_modules = {
                'os', 'sys', 'json', 'time', 'datetime', 'math', 'random', 'uuid',
                'collections', 'itertools', 'functools', 'operator', 're', 'string',
                'urllib', 'http', 'pathlib', 'typing', 'dataclasses', 'abc', 'enum',
                'threading', 'multiprocessing', 'asyncio', 'concurrent', 'queue',
                'io', 'pickle', 'csv', 'xml', 'html', 'email', 'mimetypes',
                'base64', 'binascii', 'struct', 'codecs', 'locale', 'calendar',
                'heapq', 'bisect', 'array', 'weakref', 'copy', 'pprint', 'reprlib',
                'gc', 'inspect', 'dis', 'ast', 'importlib', 'pkgutil', 'modulefinder',
                'runpy', 'site', 'builtins', '__future__', '__main__', 'warnings',
                'contextlib', 'atexit', 'traceback', 'logging', 'getopt', 'argparse',
                'configparser', 'tempfile', 'glob', 'fnmatch', 'linecache', 'shutil',
                'gzip', 'bz2', 'lzma', 'zipfile', 'tarfile', 'sqlite3', 'dbm',
                'socket', 'ssl', 'select', 'selectors', 'signal', 'subprocess',
                'sched', 'getpass', 'curses', 'platform', 'errno', 'ctypes'
            }
            base_module = import_name.split('.')[0]
            return base_module in standard_modules
        
        elif language == 'C#':
            # .NET 系统命名空间
            system_namespaces = {
                'System', 'Microsoft', 'Windows'
            }
            return any(import_name.startswith(ns) for ns in system_namespaces)
        
        elif language == 'Java':
            # Java 标准库包
            standard_packages = {
                'java.lang', 'java.util', 'java.io', 'java.net', 'java.sql',
                'java.text', 'java.time', 'java.math', 'java.security',
                'java.nio', 'java.awt', 'java.swing', 'javax.swing',
                'javax.sql', 'javax.xml', 'javax.net', 'javax.crypto'
            }
            return any(import_name.startswith(pkg) for pkg in standard_packages)
        
        elif language == 'Matlab':
            # Matlab 内置工具箱
            builtin_toolboxes = {
                'matlab', 'simulink', 'stats', 'signal', 'image', 'optimization',
                'control', 'financial', 'bioinfo', 'parallel', 'fuzzy', 'neural',
                'symbolic', 'robotics', 'audio', 'vision', 'database', 'compiler'
            }
            base_toolbox = import_name.split('.')[0]
            return base_toolbox in builtin_toolboxes
        
        return False

    def is_cross_file_import(self, import_name: str, language: str) -> bool:
        """判断是否为跨文件导入（用户代码/第三方库）"""
        if self.is_standard_import(import_name, language):
            return False
        
        if language in ['C', 'C++']:
            # 用户头文件通常用双引号或者不在标准库中
            return not import_name.startswith('<') or not self.is_standard_import(import_name, language)
        
        elif language == 'JavaScript':
            # 相对路径导入或第三方包
            return (import_name.startswith('./') or import_name.startswith('../') or
                    not self.is_standard_import(import_name, language))
        
        elif language == 'Python':
            # 非标准库的导入
            return not self.is_standard_import(import_name, language)
        
        elif language in ['C#', 'Java']:
            # 非系统命名空间的导入
            return not self.is_standard_import(import_name, language)
        
        elif language == 'Matlab':
            # 非内置工具箱的导入
            return not self.is_standard_import(import_name, language)
        
        return True

    def count_intra_file_dependencies(self, content: str, language: str) -> int:
        """统计文件内依赖（函数调用、变量引用等）"""
        # 这是一个简化的实现，可以根据需要扩展
        clean_content = self.remove_comments(content, language)
        
        intra_deps = 0
        
        if language == 'Python':
            # Python 函数调用模式
            function_calls = re.findall(r'\b(\w+)\s*\(', clean_content)
            # 过滤掉关键字和内置函数
            python_keywords = {'if', 'for', 'while', 'def', 'class', 'return', 'print', 'len', 'range', 'enumerate', 'zip', 'map', 'filter', 'sorted', 'max', 'min', 'sum', 'all', 'any', 'isinstance', 'hasattr', 'getattr', 'setattr', 'delattr', 'dir', 'vars', 'globals', 'locals', 'eval', 'exec', 'compile', 'open', 'input', 'int', 'str', 'float', 'bool', 'list', 'dict', 'set', 'tuple', 'type', 'super', 'staticmethod', 'classmethod', 'property'}
            intra_deps = len([call for call in function_calls if call not in python_keywords])
        
        elif language == 'JavaScript':
            # JavaScript 函数调用模式
            function_calls = re.findall(r'\b(\w+)\s*\(', clean_content)
            js_keywords = {'if', 'for', 'while', 'function', 'return', 'console', 'parseInt', 'parseFloat', 'isNaN', 'isFinite', 'setTimeout', 'setInterval', 'clearTimeout', 'clearInterval', 'alert', 'confirm', 'prompt', 'typeof', 'instanceof', 'new', 'delete', 'Object', 'Array', 'String', 'Number', 'Boolean', 'Date', 'RegExp', 'Math', 'JSON'}
            intra_deps = len([call for call in function_calls if call not in js_keywords])
        
        elif language in ['C', 'C++']:
            # C/C++ 函数调用模式
            function_calls = re.findall(r'\b(\w+)\s*\(', clean_content)
            c_keywords = {'if', 'for', 'while', 'return', 'printf', 'scanf', 'malloc', 'free', 'sizeof', 'strlen', 'strcpy', 'strcmp', 'strcat', 'memcpy', 'memset', 'fopen', 'fclose', 'fread', 'fwrite', 'fprintf', 'fscanf', 'cout', 'cin', 'endl', 'std'}
            intra_deps = len([call for call in function_calls if call not in c_keywords])
        
        elif language == 'Java':
            # Java 方法调用模式
            method_calls = re.findall(r'\b(\w+)\s*\(', clean_content)
            java_keywords = {'if', 'for', 'while', 'return', 'System', 'String', 'Integer', 'Double', 'Boolean', 'Math', 'Object', 'ArrayList', 'HashMap', 'HashSet', 'Scanner', 'BufferedReader', 'PrintWriter', 'StringBuilder', 'StringBuffer'}
            intra_deps = len([call for call in method_calls if call not in java_keywords])
        
        elif language == 'C#':
            # C# 方法调用模式
            method_calls = re.findall(r'\b(\w+)\s*\(', clean_content)
            csharp_keywords = {'if', 'for', 'while', 'return', 'Console', 'String', 'int', 'double', 'bool', 'Math', 'Object', 'List', 'Dictionary', 'HashSet', 'StringBuilder', 'DateTime', 'TimeSpan'}
            intra_deps = len([call for call in method_calls if call not in csharp_keywords])
        
        elif language == 'Matlab':
            # Matlab 函数调用模式
            function_calls = re.findall(r'\b(\w+)\s*\(', clean_content)
            matlab_keywords = {'if', 'for', 'while', 'return', 'disp', 'fprintf', 'sprintf', 'size', 'length', 'zeros', 'ones', 'eye', 'rand', 'randn', 'linspace', 'logspace', 'meshgrid', 'plot', 'subplot', 'figure', 'title', 'xlabel', 'ylabel', 'legend', 'sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'abs', 'max', 'min', 'sum', 'mean', 'std', 'var'}
            intra_deps = len([call for call in function_calls if call not in matlab_keywords])
        
        return intra_deps

    def analyze_file(self, file_path: Path, language: str) -> Dict[str, Any]:
        """分析单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"读取文件失败 {file_path}: {e}")
            return {}
        
        # 统计各项指标
        tokens = self.count_tokens(content)
        lines = self.count_lines(content)
        functions = self.count_functions(content, language)
        classes = self.count_classes(content, language)
        
        # 提取导入
        all_imports, standard_imports, cross_file_imports = self.extract_imports(content, language)
        
        # 统计文件内依赖
        intra_file_deps = self.count_intra_file_dependencies(content, language)
        
        return {
            'file_path': str(file_path),
            'tokens': tokens,
            'lines': lines,
            'functions': functions,
            'classes': classes,
            'imports': len(all_imports),
            'standard_imports': len(standard_imports),
            'cross_file_imports': len(cross_file_imports),
            'intra_file_dependencies': intra_file_deps,
            'all_imports_list': list(all_imports),
            'standard_imports_list': list(standard_imports),
            'cross_file_imports_list': list(cross_file_imports)
        }

    def analyze_single_project(self, project_path: Path, language: str) -> Dict[str, Any]:
        """分析单个项目"""
        extensions = self.get_project_extensions(project_path, language)
        files_analyzed = []
        ignored_files = 0
        
        project_stats = {
            'project_name': project_path.name,
            'project_path': str(project_path),
            'language': language,
            'total_files': 0,
            'tokens': 0,
            'lines': 0,
            'functions': 0,
            'classes': 0,
            'imports': 0,
            'standard_imports': 0,
            'cross_file_imports': 0,
            'intra_file_dependencies': 0,
            'ignored_files': 0,
            'files': []
        }
        
        # 检查是否为特殊项目并记录
        if project_path.name in self.special_projects:
            print(f"检测到特殊项目: {project_path.name}")
            special_config = self.special_projects[project_path.name]
            if special_config['additional_extensions']:
                print(f"  额外扩展名: {special_config['additional_extensions']}")
            if special_config['ignore_overrides']:
                print(f"  忽略规则覆盖: {special_config['ignore_overrides']}")
        
        # 遍历项目中的所有文件
        for file_path in project_path.rglob('*'):
            if file_path.is_file() and file_path.suffix in extensions:
                # 检查是否应该忽略
                if self.should_ignore_file(file_path, language, project_path):
                    ignored_files += 1
                    continue
                
                file_stats = self.analyze_file(file_path, language)
                
                if file_stats:
                    files_analyzed.append(file_stats)
                    project_stats['total_files'] += 1
                    project_stats['tokens'] += file_stats['tokens']
                    project_stats['lines'] += file_stats['lines']
                    project_stats['functions'] += file_stats['functions']
                    project_stats['classes'] += file_stats['classes']
                    project_stats['imports'] += file_stats['imports']
                    project_stats['standard_imports'] += file_stats['standard_imports']
                    project_stats['cross_file_imports'] += file_stats['cross_file_imports']
                    project_stats['intra_file_dependencies'] += file_stats['intra_file_dependencies']
        
        project_stats['files'] = files_analyzed
        project_stats['ignored_files'] = ignored_files
        
        return project_stats

    def analyze_language_projects(self, language: str) -> Dict[str, Any]:
        """分析某个语言下的所有项目"""
        language_path = self.base_path / language
        
        if not language_path.exists():
            print(f"语言目录不存在: {language_path}")
            return {}
        
        print(f"开始分析 {language} 语言下的项目...")
        
        language_results = {
            'language': language,
            'total_projects': 0,
            'projects': {}
        }
        
        # 遍历语言目录下的所有项目
        project_dirs = [d for d in language_path.iterdir() if d.is_dir()]
        
        for project_dir in project_dirs:
            project_name = project_dir.name
            print(f"  分析项目: {project_name}")
            
            project_stats = self.analyze_single_project(project_dir, language)
            
            if project_stats['total_files'] > 0:
                language_results['projects'][project_name] = project_stats
                language_results['total_projects'] += 1
                
                print(f"    完成: {project_stats['total_files']} 文件, "
                      f"{project_stats['tokens']} tokens, "
                      f"{project_stats['functions']} 函数, "
                      f"{project_stats['classes']} 类")
            else:
                print(f"    跳过: {project_name} (无有效文件)")
        
        print(f"{language} 语言分析完成: {language_results['total_projects']} 个项目")
        return language_results

    def calculate_statistics(self, values: List[float]) -> Dict[str, float]:
        """计算统计量"""
        if not values:
            return {}
        
        stats = {
            'count': len(values),
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'min': min(values),
            'max': max(values),
            'std': statistics.stdev(values) if len(values) > 1 else 0.0
        }
        
        # 添加分位数
        if len(values) >= 4:
            sorted_values = sorted(values)
            n = len(sorted_values)
            stats['q1'] = sorted_values[n // 4]
            stats['q3'] = sorted_values[3 * n // 4]
        
        return stats

    def analyze_all_projects(self) -> Dict[str, Any]:
        """分析所有语言的项目"""
        results = {}
        
        for language in self.language_extensions.keys():
            results[language] = self.analyze_language_projects(language)
        
        return results

    def generate_statistics_report(self, results: Dict[str, Any]) -> str:
        """生成统计报告"""
        report_lines = []
        report_lines.append("=" * 100)
        report_lines.append("项目复杂度统计报告")
        report_lines.append("=" * 100)
        
        # 添加特殊项目处理说明
        report_lines.append("\n特殊项目处理:")
        report_lines.append("-" * 50)
        for project_name, config in self.special_projects.items():
            report_lines.append(f"项目: {project_name} ({config['language']})")
            if config['additional_extensions']:
                report_lines.append(f"  额外扩展名: {', '.join(config['additional_extensions'])}")
            if config['ignore_overrides']:
                for override_type, override_list in config['ignore_overrides'].items():
                    report_lines.append(f"  {override_type}: {', '.join(override_list)}")
        
        # 定义要统计的指标
        metrics = ['tokens', 'lines', 'functions', 'classes', 'imports', 
                  'standard_imports', 'cross_file_imports', 'intra_file_dependencies']
        
        metric_names = {
            'tokens': 'Tokens',
            'lines': 'Lines',
            'functions': 'Functions',
            'classes': 'Classes',
            'imports': 'Total Imports',
            'standard_imports': 'Standard Library Imports',
            'cross_file_imports': 'Cross-file Imports',
            'intra_file_dependencies': 'Intra-file Dependencies'
        }
        
        # 各语言统计
        for language, lang_data in results.items():
            if not lang_data or lang_data['total_projects'] == 0:
                continue
            
            report_lines.append(f"\n{'=' * 80}")
            report_lines.append(f"{language} 语言统计 ({lang_data['total_projects']} 个项目)")
            report_lines.append(f"{'=' * 80}")
            
            # 收集每个项目的各项指标
            project_metrics = {metric: [] for metric in metrics}
            
            for project_name, project_stats in lang_data['projects'].items():
                for metric in metrics:
                    if metric in project_stats:
                        project_metrics[metric].append(project_stats[metric])
            
            # 计算并显示统计量
            for metric in metrics:
                if project_metrics[metric]:
                    stats = self.calculate_statistics(project_metrics[metric])
                    report_lines.append(f"\n{metric_names[metric]}:")
                    report_lines.append(f"  平均值: {stats['mean']:.2f}")
                    report_lines.append(f"  中位数: {stats['median']:.2f}")
                    report_lines.append(f"  最小值: {stats['min']:.0f}")
                    report_lines.append(f"  最大值: {stats['max']:.0f}")
                    report_lines.append(f"  标准差: {stats['std']:.2f}")
                    if 'q1' in stats and 'q3' in stats:
                        report_lines.append(f"  第1四分位数: {stats['q1']:.2f}")
                        report_lines.append(f"  第3四分位数: {stats['q3']:.2f}")
            
            # 显示项目详情
            report_lines.append(f"\n{'-' * 60}")
            report_lines.append(f"项目详情:")
            report_lines.append(f"{'-' * 60}")
            
            # 按tokens数量排序
            projects = list(lang_data['projects'].items())
            projects.sort(key=lambda x: x[1]['tokens'], reverse=True)
            
            for project_name, project_stats in projects:
                report_lines.append(f"\n项目: {project_name}")
                report_lines.append(f"  文件数: {project_stats['total_files']}")
                
                # 标记特殊项目
                if project_name in self.special_projects:
                    report_lines.append(f"  [特殊项目处理]")
                
                for metric in metrics:
                    if metric in project_stats:
                        report_lines.append(f"  {metric_names[metric]}: {project_stats[metric]}")
        
        return '\n'.join(report_lines)

    def save_results(self, results: Dict[str, Any], output_file: str = "enhanced_complexity_analysis.json"):
        """保存结果到JSON文件"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"结果已保存到: {output_file}")

    def generate_csv_report(self, results: Dict[str, Any], output_file: str = "project_statistics.csv"):
        """生成CSV格式的统计报告"""
        import csv
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Language', 'Project', 'Special_Project', 'Files', 'Tokens', 'Lines', 'Functions', 
                         'Classes', 'Total_Imports', 'Standard_Imports', 'Cross_File_Imports', 
                         'Intra_File_Dependencies']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for language, lang_data in results.items():
                if not lang_data or lang_data['total_projects'] == 0:
                    continue
                
                for project_name, project_stats in lang_data['projects'].items():
                    is_special = project_name in self.special_projects
                    writer.writerow({
                        'Language': language,
                        'Project': project_name,
                        'Special_Project': 'Yes' if is_special else 'No',
                        'Files': project_stats['total_files'],
                        'Tokens': project_stats['tokens'],
                        'Lines': project_stats['lines'],
                        'Functions': project_stats['functions'],
                        'Classes': project_stats['classes'],
                        'Total_Imports': project_stats['imports'],
                        'Standard_Imports': project_stats['standard_imports'],
                        'Cross_File_Imports': project_stats['cross_file_imports'],
                        'Intra_File_Dependencies': project_stats['intra_file_dependencies']
                    })
        
        print(f"CSV报告已保存到: {output_file}")

    def generate_summary_statistics(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """生成按语言汇总的统计信息"""
        summary = {}
        
        metrics = ['tokens', 'lines', 'functions', 'classes', 'imports', 
                  'standard_imports', 'cross_file_imports', 'intra_file_dependencies']
        
        for language, lang_data in results.items():
            if not lang_data or lang_data['total_projects'] == 0:
                continue
            
            # 收集该语言所有项目的指标
            project_metrics = {metric: [] for metric in metrics}
            
            for project_name, project_stats in lang_data['projects'].items():
                for metric in metrics:
                    if metric in project_stats:
                        project_metrics[metric].append(project_stats[metric])
            
            # 计算统计量
            language_stats = {}
            for metric in metrics:
                if project_metrics[metric]:
                    language_stats[metric] = self.calculate_statistics(project_metrics[metric])
            
            summary[language] = {
                'total_projects': lang_data['total_projects'],
                'statistics': language_stats
            }
        
        return summary

    def print_summary_table(self, results: Dict[str, Any]):
        """打印汇总统计表格"""
        summary = self.generate_summary_statistics(results)
        
        print("\n" + "=" * 120)
        print("各语言项目统计汇总表")
        print("=" * 120)
        
        # 表头
        header = f"{'Language':<12} {'Projects':<9} {'Tokens':<12} {'Lines':<12} {'Functions':<10} {'Classes':<8} {'Imports':<8} {'Std-Lib':<8} {'Cross-File':<10} {'Intra-File':<10}"
        print(header)
        print("-" * 130)
        
        # 数据行
        for language, lang_summary in summary.items():
            if 'statistics' in lang_summary:
                stats = lang_summary['statistics']
                
                # 获取各指标的平均值
                tokens_avg = stats.get('tokens', {}).get('mean', 0)
                lines_avg = stats.get('lines', {}).get('mean', 0)
                functions_avg = stats.get('functions', {}).get('mean', 0)
                classes_avg = stats.get('classes', {}).get('mean', 0)
                imports_avg = stats.get('imports', {}).get('mean', 0)
                std_imports_avg = stats.get('standard_imports', {}).get('mean', 0)
                cross_file_avg = stats.get('cross_file_imports', {}).get('mean', 0)
                intra_file_avg = stats.get('intra_file_dependencies', {}).get('mean', 0)
                
                row = f"{language:<12} {lang_summary['total_projects']:<9} {tokens_avg:<12.1f} {lines_avg:<12.1f} {functions_avg:<10.1f} {classes_avg:<8.1f} {imports_avg:<8.1f} {std_imports_avg:<8.1f} {cross_file_avg:<10.1f} {intra_file_avg:<10.1f}"
                print(row)
        
        print("-" * 130)
        
        # 打印详细统计信息
        print("\n详细统计信息:")
        print("=" * 80)
        
        for language, lang_summary in summary.items():
            if 'statistics' in lang_summary:
                print(f"\n{language} 语言 ({lang_summary['total_projects']} 个项目):")
                print("-" * 50)
                
                stats = lang_summary['statistics']
                metrics_display = {
                    'tokens': 'Tokens',
                    'lines': 'Lines', 
                    'functions': 'Functions',
                    'classes': 'Classes',
                    'imports': 'Total Imports',
                    'standard_imports': 'Standard Library Imports',
                    'cross_file_imports': 'Cross-file Imports',
                    'intra_file_dependencies': 'Intra-file Dependencies'
                }
                
                for metric, display_name in metrics_display.items():
                    if metric in stats:
                        s = stats[metric]
                        print(f"  {display_name}:")
                        print(f"    平均值: {s['mean']:.2f}, 中位数: {s['median']:.2f}")
                        print(f"    最小值: {s['min']:.0f}, 最大值: {s['max']:.0f}")
                        print(f"    标准差: {s['std']:.2f}")
                        if 'q1' in s and 'q3' in s:
                            print(f"    四分位数: Q1={s['q1']:.2f}, Q3={s['q3']:.2f}")
                        print()

def main():
    """主函数"""
    # 检查是否安装了tiktoken
    try:
        import tiktoken
    except ImportError:
        print("请先安装tiktoken: pip install tiktoken")
        return
    
    # 创建分析器
    analyzer = EnhancedProjectComplexityAnalyzer()
    
    # 检查基础目录是否存在
    if not analyzer.base_path.exists():
        print(f"目录不存在: {analyzer.base_path}")
        return
    
    # 显示特殊项目处理规则
    print("特殊项目处理规则:")
    print("=" * 50)
    for project_name, config in analyzer.special_projects.items():
        print(f"项目: {project_name} ({config['language']})")
        if config['additional_extensions']:
            print(f"  额外扩展名: {', '.join(config['additional_extensions'])}")
        if config['ignore_overrides']:
            for override_type, override_list in config['ignore_overrides'].items():
                print(f"  {override_type}: {', '.join(override_list)}")
        print()
    
    # 显示忽略规则
    print("通用忽略规则:")
    print("=" * 50)
    for lang, rules in analyzer.ignore_patterns.items():
        print(f"  {lang}:")
        print(f"    忽略目录: {', '.join(rules['dirs'][:5])}...")
        print(f"    忽略文件: {', '.join(rules['files'][:3])}...")
    print()
    
    # 执行分析
    print("开始分析项目复杂度...")
    results = analyzer.analyze_all_projects()
    
    # 生成统计报告
    statistics_report = analyzer.generate_statistics_report(results)
    
    # 打印汇总统计表格
    analyzer.print_summary_table(results)
    
    # 保存结果
    analyzer.save_results(results)
    
    # 生成CSV报告
    analyzer.generate_csv_report(results)
    
    # 保存统计报告到文件
    with open("enhanced_complexity_report.txt", "w", encoding="utf-8") as f:
        f.write(statistics_report)
    
    print(f"\n分析完成！")
    print(f"详细报告已保存到: enhanced_complexity_report.txt")
    print(f"CSV数据已保存到: project_statistics.csv")
    print(f"JSON数据已保存到: enhanced_complexity_analysis.json")

if __name__ == "__main__":
    main()