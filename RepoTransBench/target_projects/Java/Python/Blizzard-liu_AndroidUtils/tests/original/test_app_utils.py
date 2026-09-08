import unittest
from unittest import mock

class PackageInfo:
    def __init__(self, versionCode=None, versionName=None):
        self.versionCode = versionCode
        self.versionName = versionName

class PackageManager:
    class NameNotFoundException(Exception):
        pass

    def __init__(self):
        self._return_info = None
        self._throw = False

    def getPackageInfo(self, name, num):
        if self._throw:
            raise PackageManager.NameNotFoundException()
        return self._return_info

class AppUtils:
    @staticmethod
    def getVerCode(context):
        try:
            pm = context.getPackageManager()
            info = pm.getPackageInfo(context.getPackageName(), 0)
            return info.versionCode
        except Exception:
            return -1

    @staticmethod
    def getVerName(context):
        try:
            pm = context.getPackageManager()
            info = pm.getPackageInfo(context.getPackageName(), 0)
            return info.versionName
        except Exception:
            return ""

class TestAppUtils(unittest.TestCase):

    def test_get_ver_code_normal(self):
        context = mock.Mock()
        pm = mock.Mock()
        info = PackageInfo(versionCode=123)
        context.getPackageName.return_value = "pkg"
        context.getPackageManager.return_value = pm
        pm.getPackageInfo.return_value = info
        self.assertEqual(123, AppUtils.getVerCode(context))

    def test_get_ver_code_not_found(self):
        context = mock.Mock()
        pm = mock.Mock()
        context.getPackageName.return_value = "pkg"
        context.getPackageManager.return_value = pm
        pm.getPackageInfo.side_effect = PackageManager.NameNotFoundException()
        self.assertEqual(-1, AppUtils.getVerCode(context))

    def test_get_ver_name_normal(self):
        context = mock.Mock()
        pm = mock.Mock()
        info = PackageInfo(versionName="verX")
        context.getPackageName.return_value = "pkg"
        context.getPackageManager.return_value = pm
        pm.getPackageInfo.return_value = info
        self.assertEqual("verX", AppUtils.getVerName(context))

    def test_get_ver_name_not_found(self):
        context = mock.Mock()
        pm = mock.Mock()
        context.getPackageName.return_value = "pkg"
        context.getPackageManager.return_value = pm
        pm.getPackageInfo.side_effect = PackageManager.NameNotFoundException()
        self.assertEqual("", AppUtils.getVerName(context))