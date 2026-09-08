// Patch so PubSub uses only standard JS and works with require()
class PubSub {
  constructor() {
    this._subscribers = Object.create(null);
  }

  subscribe(event, fn) {
    if (!this._subscribers[event]) {
      this._subscribers[event] = [];
    }
    this._subscribers[event].push(fn);
  }

  unsubscribe(event, fn) {
    if (!this._subscribers[event]) return;
    this._subscribers[event] = this._subscribers[event].filter(f => f !== fn);
  }

  publish(event, data) {
    if (!this._subscribers[event]) return;
    this._subscribers[event].forEach(fn => fn(data));
  }
}

module.exports = PubSub;