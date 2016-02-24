lazy val root = (project in file(".")).
  settings(
    name := "SolidSnake",
    version := "1.0",
    scalaVersion := "2.11.5",
    libraryDependencies +=  "net.liftweb" %% "lift-json" % "2.6",
    libraryDependencies += "org.scalactic" %% "scalactic" % "2.2.6",
    libraryDependencies += "org.scalatest" %% "scalatest" % "2.2.6" % "test"
)
