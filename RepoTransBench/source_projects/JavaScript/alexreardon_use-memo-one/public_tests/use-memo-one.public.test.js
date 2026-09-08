// @flow
import React, { type Node } from 'react';
import { mount } from 'enzyme';
import { useMemoOne } from '../src';

type WithMemoProps = {|
  inputs: mixed[],
  children: (value: mixed) => Node,
  getResult: () => mixed,
|};

function WithMemo(props: WithMemoProps) {
  const value: mixed = useMemoOne(props.getResult, props.inputs);
  return props.children(value);
}

it('should not break the cache on multiple calls with different inputs', () => {
  const mock = jest.fn().mockReturnValue(<span>hello</span>);
  const wrapper = mount(
    <WithMemo inputs={['a', 5]} getResult={() => ({ foo: 'bar' })}>
      {mock}
    </WithMemo>,
  );

  // initial call
  expect(mock).toHaveBeenCalledTimes(1);
  expect(mock).toHaveBeenCalledWith({ foo: 'bar' });
  const initial: mixed = mock.mock.calls[0][0];
  expect(initial).toEqual({ foo: 'bar' });
  mock.mockClear();

  wrapper.setProps({ inputs: ['a', 5] });

  expect(mock).toHaveBeenCalledWith(initial);
  const second: mixed = mock.mock.calls[0][0];
  // same reference
  expect(initial).toBe(second);
});

it('should break the cache when the inputs change to new array', () => {
  const mock = jest.fn().mockReturnValue(<span>hello</span>);
  const wrapper = mount(
    <WithMemo inputs={['a', 5]} getResult={() => ({ foo: 'bar' })}>
      {mock}
    </WithMemo>,
  );

  expect(mock).toHaveBeenCalledTimes(1);
  expect(mock).toHaveBeenCalledWith({ foo: 'bar' });
  const initial: mixed = mock.mock.calls[0][0];
  expect(initial).toEqual({ foo: 'bar' });
  mock.mockClear();

  // inputs are different
  wrapper.setProps({ inputs: ['a', 5, 'new'] });

  expect(mock).toHaveBeenCalledWith(initial);
  expect(mock).toHaveBeenCalledTimes(1);
  const second: mixed = mock.mock.calls[0][0];
  // different reference
  expect(initial).not.toBe(second);
});

it('should use the latest getResult function when cache breaks and return new result', () => {
  const mock = jest.fn().mockReturnValue(<span>hello</span>);
  const wrapper = mount(
    <WithMemo inputs={['a', 5]} getResult={() => ({ foo: 'bar' })}>
      {mock}
    </WithMemo>,
  );

  expect(mock).toHaveBeenCalledTimes(1);
  expect(mock).toHaveBeenCalledWith({ foo: 'bar' });
  const initial: mixed = mock.mock.calls[0][0];
  expect(initial).toEqual({ foo: 'bar' });
  mock.mockClear();

  // inputs are different (ensure a different value)
  wrapper.setProps({
    inputs: [10, 20, 30],
    getResult: () => ({ updated: 'thing' }),
  });

  expect(mock).toHaveBeenCalledWith({ updated: 'thing' });
  expect(mock).toHaveBeenCalledTimes(1);
});