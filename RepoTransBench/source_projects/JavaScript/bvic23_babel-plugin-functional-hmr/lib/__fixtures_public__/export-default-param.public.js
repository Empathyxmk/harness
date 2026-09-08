/* eslint-disable */
import { TouchableOpacity, Text } from 'react-native';
import React, { Component, PropTypes } from 'react';

export default (({ label, onTap }) => <TouchableOpacity onPress={onTap}>
        <Text style={{ color: 'red' }}>
            {label}
        </Text>
    </TouchableOpacity>);