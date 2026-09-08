import os
import sys
import pytest
from pathlib import Path

# If needed, import the main translated plugin; otherwise, mock
try:
    import src.babel_plugin_functional_hmr as plugin
    PLUGIN_AVAILABLE = True
except ImportError:
    PLUGIN_AVAILABLE = False
    plugin = None

def _fixture_path(fname):
    return Path(__file__).parent.parent / "lib" / "__fixtures_public__" / fname

def _read(fname):
    with open(_fixture_path(fname), encoding="utf-8") as f:
        return f.read()

def l(string):
    return [line for line in string.strip().split('\n') if line != '/* eslint-disable */']

def transform_js_code(source_code):
    # Placeholder: Implement actual transformation in src/babel_plugin_functional_hmr.py
    return source_code

@pytest.mark.parametrize("fixture,snapshot_name", [
    ('class-already', "already a class, should not transform anything 1"),
    ('export-default-param', "function, should transform 1"),
    ('declared-as-const', "function as const, should transform 1"),
    ('simplefunction', "simple function, should not change 1"),
    ('multiple-components', "multiple components, should change 1"),
    ('embedded-return', "embedded return, should change 1"),
])
def test_plugin_public_fixture_parity(fixture, snapshot_name, request):
    """Test plugin transformation on public fixtures using public cases."""
    source = _read(f"{fixture}.public.js")
    code = transform_js_code(source)
    result_lines = l(code)
    expected_snapshot = SNAPSHOTS[snapshot_name]
    assert result_lines == expected_snapshot

# Snapshots dictionary is subset of originals needed for public tests
SNAPSHOTS = {
    "already a class, should not transform anything 1": [
        "import { TouchableNativeFeedback, Text } from 'react-native';",
        "import React, { Component, PropTypes } from 'react';",
        "export default class Button extends Component {",
        "    render() {",
        "        return <TouchableNativeFeedback onPress={this.props.onPress}>",
        "                <Text style={{ color: 'green' }}>",
        "                    {this.props.title}",
        "                </Text>",
        "            </TouchableNativeFeedback>;",
        "    }",
        "}",
    ],
    "function, should transform 1": [
        "import { TouchableNativeFeedback, Text } from 'react-native';",
        "import React, { Component, PropTypes } from 'react';",
        "",
        "import _react from 'react';",
        "import _reactTransform from 'react-transform-hmr';",
        "",
        "function wrapComponent(id, Component) {",
        "    const t = _reactTransform({",
        "        components: {",
        "            [id]: {",
        "                displayName: id",
        "            }",
        "        },",
        "        locals: [module],",
        "        imports: [_react],",
        "        filename: '%%FILENAME%%'",
        "    });",
        "",
        "    return t(Component, id);",
        "}",
        "",
        "class __Comp extends _react.Component {",
        "    render() {",
        "        let { children, onPress } = this.props;",
        "        return (<TouchableNativeFeedback onPress={onPress}>",
        "        <Text style={{ color: 'blue' }}>",
        "            {children}",
        "        </Text>",
        "    </TouchableNativeFeedback>);",
        "    }",
        "",
        "}",
        "",
        "const Comp = wrapComponent('Comp', __Comp);",
        "export default Comp;",
    ],
    "function as const, should transform 1": [
        "import { TouchableNativeFeedback, Text } from 'react-native';",
        "import React, { Component, PropTypes } from 'react';",
        "",
        "import _react from 'react';",
        "import _reactTransform from 'react-transform-hmr';",
        "",
        "function wrapComponent(id, Component) {",
        "    const t = _reactTransform({",
        "        components: {",
        "            [id]: {",
        "                displayName: id",
        "            }",
        "        },",
        "        locals: [module],",
        "        imports: [_react],",
        "        filename: '%%FILENAME%%'",
        "    });",
        "",
        "    return t(Component, id);",
        "}",
        "",
        "class __Button extends _react.Component {",
        "    render() {",
        "        let { children, onPress } = this.props;",
        "        return (<TouchableNativeFeedback onPress={onPress}>",
        "        <Text style={{ color: 'blue' }}>",
        "            {children}",
        "        </Text>",
        "    </TouchableNativeFeedback>);",
        "    }",
        "",
        "}",
        "",
        "const Button = wrapComponent('Button', __Button);",
        "",
        "",
        "export default Button;",
    ],
    "simple function, should not change 1": [
        "export default (number => number * 2);",
    ],
    "multiple components, should change 1": [
        "import { TouchableNativeFeedback, Text } from 'react-native';",
        "import React, { Component, PropTypes } from 'react';",
        "",
        "import _react from 'react';",
        "import _reactTransform from 'react-transform-hmr';",
        "",
        "function wrapComponent(id, Component) {",
        "    const t = _reactTransform({",
        "        components: {",
        "            [id]: {",
        "                displayName: id",
        "            }",
        "        },",
        "        locals: [module],",
        "        imports: [_react],",
        "        filename: '%%FILENAME%%'",
        "    });",
        "",
        "    return t(Component, id);",
        "}",
        "",
        "class __Button extends _react.Component {",
        "    render() {",
        "        let { children, onPress } = this.props;",
        "        return (<TouchableNativeFeedback onPress={onPress}>",
        "        <Text style={{ color: 'blue' }}>",
        "            {children}",
        "        </Text>",
        "    </TouchableNativeFeedback>);",
        "    }",
        "",
        "}",
        "",
        "export const Button = wrapComponent('Button', __Button);",
        "",
        "class __Box extends _react.Component {",
        "    render() {",
        "        let { children, onPress } = this.props;",
        "        return (<TouchableNativeFeedback onPress={onPress}>",
        "        {children}",
        "    </TouchableNativeFeedback>);",
        "    }",
        "",
        "}",
        "",
        "export const Box = wrapComponent('Box', __Box);",
    ],
    "embedded return, should change 1": [
        "import { TouchableNativeFeedback, Text } from 'react-native';",
        "import React, { Component, PropTypes } from 'react';",
        "",
        "import _react from 'react';",
        "import _reactTransform from 'react-transform-hmr';",
        "",
        "function wrapComponent(id, Component) {",
        "    const t = _reactTransform({",
        "        components: {",
        "            [id]: {",
        "                displayName: id",
        "            }",
        "        },",
        "        locals: [module],",
        "        imports: [_react],",
        "        filename: '%%FILENAME%%'",
        "    });",
        "",
        "    return t(Component, id);",
        "}",
        "",
        "class __Button extends _react.Component {",
        "    render() {",
        "        return (<Text style={{ color: 'blue' }}>Test</Text>);",
        "    }",
        "",
        "}",
        "",
        "const Button = wrapComponent('Button', __Button);",
        "",
        "",
        "export default Button;",
    ]
}