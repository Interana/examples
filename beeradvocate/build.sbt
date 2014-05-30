name := "beeradvocate"

version := "1.0"

// javaOptions in run += "-Xmx12G"

resolvers += Resolver.sonatypeRepo("snapshots")

libraryDependencies += "joda-time" % "joda-time" % "2.2"

libraryDependencies += "org.joda" % "joda-convert" % "1.6"

