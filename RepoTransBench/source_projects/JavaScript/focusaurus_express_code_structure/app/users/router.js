const express = require('express');
const needUser = require('./need-user');
const router = express.Router();

router.get('/profile', needUser, function(req, res) {
  // By convention, could also get user from req.session.user
  const user = req.user || (req.session && req.session.user);
  if (!user) {
    // Should not reach here, but just in case
    return res.status(401).send('User required');
  }
  res.status(200).send('Profile: ' + user.name);
});

module.exports = router;