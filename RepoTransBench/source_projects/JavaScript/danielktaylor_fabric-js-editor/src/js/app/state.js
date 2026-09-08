// Slightly amended module for test integration
function StateModule(getState, setState) {
  if (typeof getState !== "function" || typeof setState !== "function") {
    throw new Error("getState and setState required");
  }
  let _stack = [getState()];
  let _index = 0;

  function pushState() {
    const json = getState();
    if (_stack[_index] === json) return;
    // if we have undone and add, fork history
    if (_index < _stack.length - 1) {
      _stack = _stack.slice(0, _index + 1);
    }
    _stack.push(json);
    if (_stack.length > 100) {
      _stack.shift();
    } else {
      _index++;
    }
  }

  function undo() {
    if (_index === 0) return;
    _index--;
    setState(_stack[_index]);
  }

  function redo() {
    if (_index === _stack.length - 1) return;
    _index++;
    setState(_stack[_index]);
  }

  return {
    save: pushState,
    undo,
    redo,
    // for internal test observation:
    getStack: () => _stack.slice(),
    getIndex: () => _index,
  };
}

module.exports = StateModule;