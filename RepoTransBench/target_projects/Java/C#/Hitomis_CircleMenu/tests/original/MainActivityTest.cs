using System.Reflection;
using Xunit;
using Moq;

namespace Hitomis_CircleMenu.Tests
{
    public class MainActivityTest
    {
        private MainActivity mainActivity;
        private Mock<ICircleMenu> mockCircleMenu;

        public MainActivityTest()
        {
            mainActivity = new MainActivity();
            mockCircleMenu = new Mock<ICircleMenu>();

            // Use reflection to set private field "circleMenu" to mockCircleMenu.Object
            var field = typeof(MainActivity).GetField("circleMenu", BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Public);
            if (field != null)
                field.SetValue(mainActivity, mockCircleMenu.Object);
        }

        [Fact]
        public void OnMenuOpened_CallsCircleMenuOpenMenu()
        {
            var mockMenu = new Mock<IMenu>();
            mockCircleMenu.Setup(c => c.OpenMenu()).Returns((object)null);

            bool result = mainActivity.OnMenuOpened(1, mockMenu.Object);

            mockCircleMenu.Verify(c => c.OpenMenu(), Times.Once());
        }

        [Fact]
        public void OnBackPressed_CallsCircleMenuCloseMenu()
        {
            mockCircleMenu.Setup(c => c.CloseMenu());

            mainActivity.OnBackPressed();

            mockCircleMenu.Verify(c => c.CloseMenu(), Times.Once());
        }
    }

    // Dummy interface and class declarations. In real project, use actual implementations or add project references
    public interface ICircleMenu
    {
        object OpenMenu();
        void CloseMenu();
    }
    public interface IMenu { }

    public class MainActivity
    {
        // Simulates the internal CircleMenu reference as in original Java
        private ICircleMenu circleMenu;

        public virtual bool OnMenuOpened(int id, IMenu menu)
        {
            circleMenu?.OpenMenu();
            // Return value logic not important for test; returning default
            return false;
        }
        public virtual void OnBackPressed()
        {
            circleMenu?.CloseMenu();
        }
    }
}