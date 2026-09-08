'use strict';
const AWS = require('aws-sdk');
const url = require('url');
const https = require('https');
const config = require('./config');
const _ = require('lodash');

// For testing and handler reuse: expose internals explicitly
function handleElasticBeanstalk(event, context) {
  const record = event.Records ? event.Records[0] : {};
  const sns = record.Sns || {};
  const subject = sns.Subject || 'AWS Elastic Beanstalk Notification';
  const message = sns.Message || '';
  const timestamp = sns.Timestamp || (new Date()).toISOString();

  let color = 'good';
  if (message.match(/severity|Severe|RED/i)) {
    color = 'danger';
  } else if (message.match(/info|YELLOW/i)) {
    color = 'warning';
  }

  return {
    text: subject,
    attachments: [{
      fallback: message,
      color,
      fields: [
        { title: 'Time', value: timestamp, short: true },
        { title: 'Message', value: message, short: false }
      ]
    }]
  };
}

function handleCodeDeploy(event, context) {
  const record = event.Records ? event.Records[0] : {};
  const sns = record.Sns || {};
  const subject = sns.Subject || 'AWS CodeDeploy Notification';
  let msg;
  try {
    msg = JSON.parse(sns.Message);
  } catch (e) {
    msg = sns.Message || '';
  }
  const timestamp = sns.Timestamp || (new Date()).toISOString();

  if (_.isObject(msg) && (msg.deploymentGroupName || msg.deploymentId || msg.status)) {
    let color = 'warning';
    if (msg.status === 'FAILED') color = 'danger';
    else if (msg.status === 'SUCCEEDED') color = 'good';

    return {
      text: subject,
      attachments: [{
        fallback: msg.status,
        color,
        fields: [
          { title: 'Time', value: timestamp, short: true },
          { title: 'Deployment Group', value: msg.deploymentGroupName || '', short: true },
          { title: 'Application', value: msg.applicationName || '', short: true },
          { title: 'Status', value: msg.status || '', short: true }
        ]
      }]
    };
  }
  return {
    text: subject,
    attachments: [{
      fallback: msg,
      color: 'warning',
      fields: [
        { title: 'Time', value: timestamp, short: true },
        { title: 'Message', value: typeof msg === 'string' ? msg : JSON.stringify(msg), short: false }
      ]
    }]
  };
}

function postMessage(slackUrl, message, cb) {
  const body = JSON.stringify(message);
  const options = url.parse(slackUrl);
  options.method = 'POST';
  options.headers = { 'Content-Type': 'application/json' };

  const req = https.request(options, res => {
    res.setEncoding('utf8');
    res.on('data', () => {});
    res.on('end', () => cb(null, res.statusCode));
  });
  req.on('error', e => cb(e));
  req.write(body);
  req.end();
}

module.exports = {
  handleElasticBeanstalk,
  handleCodeDeploy,
  postMessage
};