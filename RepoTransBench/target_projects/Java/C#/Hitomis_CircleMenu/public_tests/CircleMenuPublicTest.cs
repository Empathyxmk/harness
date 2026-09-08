using System.Collections.Generic;
using Xunit;

namespace Hitomis_CircleMenu.PublicTests
{
    public class CircleMenuPublicTest
    {
        private CircleMenuStub circleMenu;

        public CircleMenuPublicTest()
        {
            circleMenu = new CircleMenuStub();
        }

        [Fact]
        public void Test_SetMainMenu_DifferentColor()
        {
            circleMenu.SetMainMenu(0xFF00FF00, 200, 201);
            Assert.Equal(0xFF00FF00, circleMenu.GetMainMenuColor());
        }

        [Fact]
        public void Test_AddSubMenu_DifferentIcons()
        {
            circleMenu.AddSubMenu(0xFFFF0000, 300);
            Assert.Single(circleMenu.GetSubMenus());
            Assert.Equal(0xFFFF0000, circleMenu.GetSubMenus()[0].Color);
            Assert.Equal(300, circleMenu.GetSubMenus()[0].IconResId);
        }

        // Minimal stub for demonstration purposes
        public class CircleMenuStub
        {
            private int mainMenuColor;
            public class SubMenu { public int Color; public int IconResId; }
            private List<SubMenu> subMenus = new List<SubMenu>();
            public void SetMainMenu(int color, int iconRes, int iconRes2) { mainMenuColor = color; }
            public int GetMainMenuColor() => mainMenuColor;
            public void AddSubMenu(int color, int iconRes) => subMenus.Add(new SubMenu { Color = color, IconResId = iconRes });
            public List<SubMenu> GetSubMenus() => subMenus;
        }
    }
}