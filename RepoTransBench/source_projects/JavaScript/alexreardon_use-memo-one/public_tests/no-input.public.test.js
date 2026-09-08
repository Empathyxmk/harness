// @flow
import { useMemoOne, useCallbackOne } from '../src';
import React from 'react';
import { mount } from 'enzyme';

describe('no input hook behaviour - public', () => {
  it('useMemoOne: getResult returns number on undefined inputs', () => {
    function Comp({ getResult }) {
      const value = useMemoOne(getResult);
      return <div>{value}</div>;
    }
    const wrapper = mount(<Comp getResult={() => 100} />);
    expect(wrapper.text()).toBe('100');
    wrapper.setProps({ getResult: () => 200 });
    wrapper.update();
    expect(wrapper.text()).toBe('200');
  });

  it('useCallbackOne: callback returns function on undefined inputs', () => {
    function Comp({ callback }) {
      const fn = useCallbackOne(callback);
      return <span>{typeof fn}</span>;
    }
    const wrapper = mount(<Comp callback={() => {}} />);
    expect(wrapper.text()).toBe('function');
  });
});