// Pure CommonJS version for node/test/coverage
const slice = require('./array').slice;

// Ported Queue implementation avoiding any ESM syntax
function Queue(size) {
  this._size = size;
  this._call = this._error = null;
  this._tasks = [];
  this._data = [];
  this._waiting = this._active = this._ended = this._start = 0;
}

// Add new task to queue
Queue.prototype.defer = function(callback) {
  if (typeof callback !== "function") throw new TypeError("callback is not a function");
  if (this._call) throw new Error("defer after await");
  this._tasks.push(callback);
  ++this._waiting;
  this._maybeNotify();
  return this; // For chaining
};

Queue.prototype._maybeNotify = function() {
  // This runs tasks up to concurrency
  while (this._active < this._size && this._waiting) {
    var i = this._tasks.length - this._waiting;
    var task = this._tasks[i];
    this._waiting--;
    this._active++;
    var self = this;
    if (typeof setImmediate === "function") {
      setImmediate(function() {
        self._runTask(i, task);
      });
    } else {
      process.nextTick(function() {
        self._runTask(i, task);
      });
    }
  }
};

Queue.prototype._runTask = function(i, task) {
  var self = this;
  try {
    task(function(error, result) {
      self._active--;
      self._ended++;
      if (!self._call) return;
      if (error) {
        self._call(error);
        self._call = null;
      } else {
        self._data[i] = result;
        if (self._ended === self._tasks.length) {
          self._call(null, slice.call(self._data));
        } else {
          self._maybeNotify();
        }
      }
    });
  } catch (e) {
    if (this._call) {
      this._call(e);
      this._call = null;
    }
  }
};

Queue.prototype.awaitAll = function(callback) {
  if (this._call) throw new Error("multiple await");
  this._call = callback;
  if (this._ended === this._tasks.length) {
    this._call(null, slice.call(this._data));
  } else {
    this._maybeNotify();
  }
  return this;
};

module.exports = {
  queue: function(size) {
    return new Queue(size || 1); // default concurrency=1
  }
};