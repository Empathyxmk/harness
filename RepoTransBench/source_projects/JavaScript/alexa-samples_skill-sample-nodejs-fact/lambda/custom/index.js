/*
 * Copyright 2018-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */

// sets up dependencies
const Alexa = require('ask-sdk-core');
const i18n = require('i18next');
const sprintf = require('i18next-sprintf-postprocessor');
/* personalization Utility avaialabe when skill personalization is turned on*/
const personalizationUtil = require('./personalizationUtil')
const personalizationStorageUtil = require('./personalizationStorageUtil')
/* constants */
const DEFAULT_TOPIC = "SPACE"
const FACT_TYPE = "factType"

// declaring picture URLs for each planet
const planetURLs =
  [
    'https://public-eu-west-1.s3.eu-west-1.amazonaws.com/pictures/planets/mercury.jpg',
    'https://public-eu-west-1.s3.eu-west-1.amazonaws.com/pictures/planets/venus.jpg',
    'https://public-eu-west-1.s3.eu-west-1.amazonaws.com/pictures/planets/mars.jpg',
    'https://public-eu-west-1.s3.eu-west-1.amazonaws.com/pictures/planets/jupiter.jpg',
    'https://public-eu-west-1.s3.eu-west-1.amazonaws.com/pictures/planets/sun.jpg',
  ]

// helper functions for supported interfaces
function supportsInterface(handlerInput, interfaceName) {
  const interfaces = ((((
    handlerInput.requestEnvelope && handlerInput.requestEnvelope.context || {})
    .System || {})
    .device || {})
    .supportedInterfaces || {});
  return interfaces[interfaceName] !== null && interfaces[interfaceName] !== undefined;
}
function supportsAPL(handlerInput) {
  return supportsInterface(handlerInput, 'Alexa.Presentation.APL')
}

module.exports.supportsInterface = supportsInterface;
module.exports.supportsAPL = supportsAPL;