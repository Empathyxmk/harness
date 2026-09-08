// Middleware to ensure req.session.user exists
module.exports = function needUser(req, res, next) {
  // Accept both req.user or req.session.user for backwards compatibility in code/tests
  if ((req.session && req.session.user) || req.user) {
    next();
    return;
  }
  res.status(401).send('User required');
};