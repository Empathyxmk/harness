import { TouchableOpacity, Text } from 'react-native';
import React, { Component, PropTypes } from 'react';

const Link = ({ label, onTap }) =>
    <TouchableOpacity onPress={onTap}>
        <Text style={{ color: 'red' }}>
            {label}
        </Text>
    </TouchableOpacity>;

export default Link;