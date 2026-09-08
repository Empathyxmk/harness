using System;
using System.IO;

public static class TestUtilities
{
    public static string CaptureConsoleOutput(Action toRun)
    {
        var currentOut = Console.Out;
        using (var sw = new StringWriter())
        {
            Console.SetOut(sw);
            toRun();
            Console.SetOut(currentOut);
            return sw.ToString();
        }
    }
}