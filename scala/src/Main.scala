package dataops.quality

import java.nio.file.{Files, Path, Paths}
import scala.jdk.CollectionConverters.*
import scala.util.Try

/** Contrôle qualité des incidents de DataOps Memory.
  *
  * Les lectures de fichiers sont regroupées ici, au bord du programme ;
  * toutes les règles sont des fonctions pures dans ContentChecks.
  *
  * Usage : scala-cli run scala --main-class dataops.quality.checkIncidents -- [dossier data] [dossier des icônes]
  */
@main def checkIncidents(arguments: String*): Unit =
  val dataDir = arguments.lift(0).getOrElse(DefaultDataDir)
  val iconsDir = arguments.lift(1).getOrElse(DefaultIconsDir)
  val result =
    for
      french <- loadIncidents(Paths.get(dataDir, "incidents.json"))
      english <- loadIncidents(Paths.get(dataDir, "incidents_en.json"))
    yield Report.build(french, english, listIcons(Paths.get(iconsDir)))

  result match
    case Left(errors) =>
      errors.foreach(error => println(s"ERREUR : $error"))
      sys.exit(1)
    case Right(report) =>
      println(report.render)
      if !report.isValid then sys.exit(1)

val DefaultDataDir = "data"
val DefaultIconsDir = "assets/icons"

private def loadIncidents(path: Path): Either[List[String], List[Incident]] =
  for
    text <- Try(Files.readString(path)).toEither.left.map(_ => List(s"fichier introuvable : $path"))
    records <- FlatJson.parseRecords(text).left.map(message => List(s"$path : $message"))
    incidents <- Incident.fromRecords(records)
  yield incidents

private def listIcons(folder: Path): Set[String] =
  Try(Files.list(folder).iterator.asScala.map(_.getFileName.toString).toSet).getOrElse(Set.empty)
