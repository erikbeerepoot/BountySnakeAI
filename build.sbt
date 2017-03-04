lazy val root = (project in file(".")).
  settings(
    name := "ScalaSnake",
    version := "1.0",
    scalaVersion := "2.11.6",
    scalacOptions := Seq("-unchecked", "-deprecation", "-encoding", "utf8","-optimize"),



      libraryDependencies ++= {
      val akkaV = "2.3.9"
      val sprayV = "1.3.3"
      Seq(
        "net.liftweb" %% "lift-json" % "2.6",
        "org.scalactic" %% "scalactic" % "2.2.6",
        "org.scalatest" %% "scalatest" % "2.2.6" % "test",
        "io.spray"            %%  "spray-can"     % sprayV,
        "io.spray"            %%  "spray-routing" % sprayV,
        "io.spray"            %%  "spray-testkit" % sprayV  % "test",
        "com.typesafe.akka"   %%  "akka-actor"    % akkaV,
        "com.typesafe.akka"   %%  "akka-testkit"  % akkaV   % "test",
        "org.specs2"          %%  "specs2-core"   % "2.3.11" % "test",
        "io.spray"            %%  "spray-json"    % "1.3.2"
      )
    }
  ).enablePlugins(SbtTwirl,JavaAppPackaging)
  Revolver.settings
