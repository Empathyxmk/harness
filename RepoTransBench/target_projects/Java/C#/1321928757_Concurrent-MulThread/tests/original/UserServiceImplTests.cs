using System.Collections.Generic;
using System.Linq;
using Xunit;

namespace OriginalTests
{
    // Dummy implementation for testing — replace with actual application implementations.
    public class UserDO
    {
        public string UserName { get; set; }
    }

    public class UserReq
    {
        public string UserName { get; set; }
    }

    public class UserServiceImpl
    {
        private readonly List<UserDO> _users = new List<UserDO>();
        public bool Add(UserReq req)
        {
            if (req == null || string.IsNullOrWhiteSpace(req.UserName))
                return false;
            // In the Java test, adding a duplicate user is allowed (assertTrue even for duplicate names)
            _users.Add(new UserDO { UserName = req.UserName });
            return true;
        }

        public List<UserDO> QueryAll() => _users.ToList();
    }

    public class UserServiceImplTests
    {
        private UserServiceImpl _userService;

        public UserServiceImplTests()
        {
            _userService = new UserServiceImpl();
            // pre-populate with a user for these tests
            var req = new UserReq { UserName = "alice" };
            _userService.Add(req);
        }

        [Fact]
        public void TestAddUser()
        {
            var req = new UserReq { UserName = "bob" };
            var result = _userService.Add(req);
            Assert.True(result);

            var users = _userService.QueryAll();
            Assert.Contains(users, u => u.UserName == "bob");
        }

        [Fact]
        public void TestQueryAll()
        {
            var users = _userService.QueryAll();
            Assert.NotNull(users);
            Assert.NotEmpty(users);
        }

        [Fact]
        public void TestAddDuplicateUser()
        {
            var req = new UserReq { UserName = "alice" }; // "alice" is added in constructor
            var result = _userService.Add(req);
            Assert.True(result); // allowed in the sample
        }
    }
}