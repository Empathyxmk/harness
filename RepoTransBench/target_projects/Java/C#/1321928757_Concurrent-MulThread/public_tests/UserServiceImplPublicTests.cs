using System.Collections.Generic;
using System.Linq;
using Xunit;

namespace PublicTests
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
            // Adding a duplicate user is allowed
            _users.Add(new UserDO { UserName = req.UserName });
            return true;
        }

        public List<UserDO> QueryAll() => _users.ToList();
    }

    public class UserServiceImplPublicTests
    {
        private readonly UserServiceImpl _userService;

        public UserServiceImplPublicTests()
        {
            _userService = new UserServiceImpl();
            // Pre-populate user for public test
            var req = new UserReq { UserName = "publicuser" };
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
            var req = new UserReq { UserName = "publicuser" };
            var result = _userService.Add(req);
            Assert.True(result);
        }
    }
}