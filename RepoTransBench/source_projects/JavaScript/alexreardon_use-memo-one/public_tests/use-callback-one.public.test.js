// @flow
import React, { type Node } from 'react';
import { mount } from 'enzyme';
import { useCallbackOne } from '../src';

type Props = {|
  inputs: mixed[],
  children: (value: mixed) => Node,
  callback: Function,
|};

function WithCallback(props: Props) {
  const fn: Function = useCallbackOne(props.callback, props.inputs);
  return props.children(fn);
}

it('should return the passed callback until input changes (using string/boolean inputs)', () => {
  const mock = jest.fn().mockReturnValue(<span>hi</span>);
  const callback = () => {};
  const wrapper = mount(
    <WithCallback inputs={['x', true]} callback={callback}>
      {mock}
    </WithCallback>,
  );

  expect(mock).toHaveBeenCalledTimes(1);
  expect(mock).toHaveBeenCalledWith(callback);
  const first: mixed = mock.mock.calls[0][0];
  expect(first).toBe(callback);

  mock.mockClear();
  // no input change
  wrapper.setProps({ inputs: ['x', true], callback: () => ({ baz: 'qux' }) });

  expect(mock).toHaveBeenCalledTimes(1);
  const second: mixed = mock.mock.calls[0][0];
  expect(second).toBe(first);

  mock.mockClear();

  // input change
  const newCallback = () => {};
  wrapper.setProps({ inputs: ['x', false], callback: newCallback });

  expect(mock).toHaveBeenCalledTimes(1);
  const third: mixed = mock.mock.calls[0][0];
  expect(third).toBe(newCallback);
});