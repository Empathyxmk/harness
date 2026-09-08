using System.Reflection;
using Xunit;
using Moq;

namespace Hitomis_CircleMenu.PublicTests
{
    public class MainActivityPublicTest
    {
        private MainActivity mainActivity;
        private Mock<ICircleMenu> mockCircleMenu;

        public MainActivityPublicTest()
        {
            mainActivity = new MainActivity();
            mockCircleMenu = new Mock<ICircleMenu>();

            var field = typeof(MainActivity).GetField("circleMenu", BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Public);
            if (field != null)
                field.SetValue(mainActivity, mockCircleMenu.Object);
        }

        [Fact]
        public void OnMenuOpened_CallsOpenMenu_Twice()
        {
            var mockMenu = new Mock<IMenu>();
            mockCircleMenu.Setup(c => c.OpenMenu()).Returns((object)null);

            mainActivity.OnMenuOpened(2, mockMenu.Object);
            mainActivity.OnMenuOpened(3, mockMenu.Object);

            mockCircleMenu.Verify(c => c.OpenMenu(), Times.Exactly(2));
        }

        [Fact]
        public void OnBackPressed_CallsCircleMenuCloseMenu_MultipleTimes()
        {
            mockCircleMenu.Setup(c => c.CloseMenu());

            mainActivity.OnBackPressed();
            mainActivity.OnBackPressed();

            mockCircleMenu.Verify(c => c.CloseMenu(), Times.Exactly(2));
        }
    }

    // Dummy interface and class declarations, similar to original/ see MainActivityTest
    public interface ICircleMenu { object OpenMenu(); void CloseMenu(); }
    public interface IMenu { }
    public class MainActivity
    {
        private ICircleMenu circleMenu;
        public virtual bool OnMenuOpened(int id, IMenu menu) { circleMenu?.OpenMenu(); return false; }
        public virtual void OnBackPressed() { circleMenu?.CloseMenu(); }
    }
}