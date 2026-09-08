/* eslint-disable */
import { TouchableOpacity, Text } from 'react-native';
import React, { Component, PropTypes } from 'react';
export default class Link extends Component {
    render() {
        return (
            <TouchableOpacity onPress={this.props.onPress}>
                <Text style={{ color: 'red' }}>
                    {this.props.label}
                </Text>
            </TouchableOpacity>
        );
    }
}