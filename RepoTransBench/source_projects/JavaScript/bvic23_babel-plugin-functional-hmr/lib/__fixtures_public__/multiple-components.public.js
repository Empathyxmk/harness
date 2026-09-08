import { TouchableOpacity, Text } from 'react-native';
import React, { Component, PropTypes } from 'react';

export const Link = ({ children, onTap }) =>
    <TouchableOpacity onPress={onTap}>
        <Text style={{ color: 'red' }}>
            {children}
        </Text>
    </TouchableOpacity>;

export const Card = ({ children, onTap }) =>
    <TouchableOpacity onPress={onTap}>
        {children}
    </TouchableOpacity>;