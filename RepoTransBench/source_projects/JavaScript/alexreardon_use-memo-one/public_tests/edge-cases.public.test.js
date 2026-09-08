// @flow
import { useMemoOne, useCallbackOne } from '../src';
import React from 'react';
import { mount } from 'enzyme';

describe('useMemoOne edge cases (public)', () => {
  function MemoComp({ getResult, inputs }) {
    const value = useMemoOne(getResult, inputs);
    return <span>{JSON.stringify(value)}</span>;
  }

  it('handles undefined inputs and different return value', () => {
    const getResult = jest.fn(() => 12345);
    const wrapper = mount(<MemoComp getResult={getResult} />);
    expect(wrapper.text()).toBe('12345');
    wrapper.setProps({ getResult: () => 67890 });
    wrapper.update();
    expect(wrapper.text()).toBe('67890');
  });

  it('works with objects and falsy values in inputs', () => {
    const getResult = jest.fn(() => 'otherVal');
    const obj = { z: 9 };
    const wrapper = mount(<MemoComp getResult={getResult} inputs={[obj, false, 0]} />);
    expect(wrapper.text()).toBe('"otherVal"');
    wrapper.setProps({ inputs: [obj, false, 1] });
    wrapper.update();
    expect(wrapper.text()).toBe('"otherVal"');
  });
});

describe('useCallbackOne edge cases (public)', () => {
  function CallbackComp({ callback, inputs }) {
    const fn = useCallbackOne(callback, inputs);
    return <span>{typeof fn}</span>;
  }

  it('handles empty array for inputs', () => {
    const callback = jest.fn();
    const wrapper = mount(<CallbackComp callback={callback} inputs={[]} />);
    expect(wrapper.text()).toBe('function');
  });

  it('returns new callback if inputs changes with objects', () => {
    const callback = jest.fn();
    const wrapper = mount(<CallbackComp callback={callback} inputs={[{ a: 1 }, 0]} />);
    const firstFn = wrapper.find('span').text();
    wrapper.setProps({ inputs: [{ a: 2 }, 0] });
    wrapper.update();
    const afterFn = wrapper.find('span').text();
    expect(afterFn).toBe(firstFn);
  });
});