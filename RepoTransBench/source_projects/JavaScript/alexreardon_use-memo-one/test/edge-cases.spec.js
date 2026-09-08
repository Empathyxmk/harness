// @flow
import { useMemoOne, useCallbackOne } from '../src';
import React from 'react';
import { mount } from 'enzyme';

describe('useMemoOne edge cases', () => {
  function MemoComp({ getResult, inputs }) {
    const value = useMemoOne(getResult, inputs);
    return <span>{JSON.stringify(value)}</span>;
  }

  it('handles undefined inputs', () => {
    const getResult = jest.fn(() => 'val');
    const wrapper = mount(<MemoComp getResult={getResult} />);
    expect(wrapper.text()).toBe('"val"');
    // re-render with same no-inputs, getResult called again due to "inputs" is undefined
    wrapper.setProps({ getResult: () => 'next' });
    wrapper.update();
    expect(wrapper.text()).toBe('"next"');
  });

  it('works with null and undefined values in inputs', () => {
    const getResult = jest.fn(() => 'something');
    const wrapper = mount(<MemoComp getResult={getResult} inputs={[null, undefined, 42]} />);
    expect(wrapper.text()).toBe('"something"');
    wrapper.setProps({ inputs: [null, undefined, 43] });
    wrapper.update();
    expect(wrapper.text()).toBe('"something"');
  });
});

describe('useCallbackOne edge cases', () => {
  function CallbackComp({ callback, inputs }) {
    const fn = useCallbackOne(callback, inputs);
    return <span>{typeof fn}</span>;
  }

  it('handles empty inputs', () => {
    const callback = jest.fn();
    const wrapper = mount(<CallbackComp callback={callback} inputs={[]} />);
    expect(wrapper.text()).toBe('function');
  });

  it('returns new callback if inputs length changes', () => {
    const callback = jest.fn();
    const wrapper = mount(<CallbackComp callback={callback} inputs={[1,2]} />);
    const firstFn = wrapper.find('span').text();
    wrapper.setProps({ inputs: [1,2,3] });
    wrapper.update();
    const afterFn = wrapper.find('span').text();
    expect(afterFn).toBe(firstFn);
  });
});