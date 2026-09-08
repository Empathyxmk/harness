const { expect } = require('chai');
const { parse } = require('../lib/profile');

describe('Profile parse', () => {
  it('should parse JSON object', () => {
    const json = {
      id: 42,
      id_str: '42str',
      screen_name: 'user',
      name: 'User Name',
      email: 'user@example.com',
      profile_image_url_https: 'https://img/x.jpg'
    };
    const profile = parse(json);
    expect(profile.id).to.equal('42str');
    expect(profile.username).to.equal('user');
    expect(profile.displayName).to.equal('User Name');
    expect(profile.emails[0].value).to.equal('user@example.com');
    expect(profile.photos[0].value).to.equal('https://img/x.jpg');
  });

  it('should use id if id_str is not present', () => {
    const json = {
      id: 100,
      screen_name: 'foo',
      name: 'FOO',
      profile_image_url_https: 'x',
    };
    const profile = parse(json);
    expect(profile.id).to.equal('100');
    expect(profile.username).to.equal('foo');
    expect(profile.displayName).to.equal('FOO');
    expect(profile.emails).to.equal(undefined);
    expect(profile.photos[0].value).to.equal('x');
  });

  it('should parse from string', () => {
    const obj = {
      id: 7,
      id_str: 'seven',
      screen_name: 'seven',
      name: 'Sev',
      profile_image_url_https: 'https://pic/7.jpg'
    };
    const str = JSON.stringify(obj);
    const profile = parse(str);
    expect(profile.id).to.equal('seven');
    expect(profile.username).to.equal('seven');
    expect(profile.displayName).to.equal('Sev');
    expect(profile.photos[0].value).to.equal('https://pic/7.jpg');
  });
});