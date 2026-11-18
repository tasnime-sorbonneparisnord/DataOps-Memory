package dataops.quality

/** Tests de l'extension Scala, avec de simples assert (comme dans le cours).
  *
  * Lancement : scala-cli run scala --main-class dataops.quality.runQualityTests
  */
@main def runQualityTests(): Unit =
  val tests: List[(String, () => Unit)] = List(
    "le JSON plat est lu avec les accents et les échappements" -> parsesFlatJson,
    "un JSON mal formé donne une erreur claire, pas une exception" -> rejectsBrokenJson,
    "une paire sans champ obligatoire est refusée" -> rejectsMissingField,
    "les pair_id en double sont détectés" -> findsDuplicates,
    "les paires sont comptées par thème" -> countsByTheme,
    "un texte trop long pour une carte est signalé" -> findsLongLabels,
    "une icône absente du dossier est signalée" -> findsMissingIcons,
    "une paire manquante dans une langue est signalée" -> findsTranslationGaps,
    "un thème différent entre les langues est signalé" -> findsTranslationMismatches,
    "un contenu correct ne donne aucun problème" -> validContentHasNoProblem
  )
  val failures = tests.flatMap { (name, test) =>
    try
      test()
      println(s"  OK    $name")
      None
    catch case error: AssertionError =>
      println(s"  ÉCHEC $name : ${error.getMessage}")
      Some(name)
  }
  println(s"${tests.size - failures.size} / ${tests.size} tests réussis")
  if failures.nonEmpty then sys.exit(1)

private def pair(id: String, theme: String = "database", incident: String = "Disque plein",
                 icon: String = "database_incident.png"): Incident =
  Incident(id, theme, incident, "Purger les logs", "Explication", icon, "database_solution.png")

private val icons = Set("database_incident.png", "database_solution.png")
private val twelvePairs = (1 to 12).toList.map(number => pair(f"DB-$number%02d"))

private def parsesFlatJson(): Unit =
  val text = """[ {"pair_id": "DB-01", "incident": "Requête \"lente\"\n", "theme": "café"} ]"""
  val records = FlatJson.parseRecords(text)
  assert(records == Right(List(Map("pair_id" -> "DB-01", "incident" -> "Requête \"lente\"\n", "theme" -> "café"))), records)

private def rejectsBrokenJson(): Unit =
  assert(FlatJson.parseRecords("""[ {"pair_id": "DB-01" ]""").isLeft)
  assert(FlatJson.parseRecords("""[ {"pair_id": 12} ]""").isLeft)
  assert(FlatJson.parseRecords("[] en trop").isLeft)

private def rejectsMissingField(): Unit =
  val result = Incident.fromRecords(List(Map("pair_id" -> "DB-01", "theme" -> "database")))
  assert(result.left.exists(_.head.contains("incident")), result)

private def findsDuplicates(): Unit =
  assert(ContentChecks.duplicatePairIds(List(pair("A"), pair("B"), pair("A"))) == Set("A"))

private def countsByTheme(): Unit =
  val counts = ContentChecks.pairsByTheme(List(pair("A"), pair("B", theme = "cloud"), pair("C")))
  assert(counts == Map("database" -> 2, "cloud" -> 1), counts)

private def findsLongLabels(): Unit =
  val tooLong = "x" * (ContentChecks.MaxLabelLength + 1)
  assert(ContentChecks.labelsTooLong(List(pair("A", incident = tooLong))) == List(tooLong))

private def findsMissingIcons(): Unit =
  assert(ContentChecks.missingIcons(List(pair("A", icon = "cloud_incident.png")), icons) == Set("cloud_incident.png"))

private def findsTranslationGaps(): Unit =
  assert(ContentChecks.translationGaps(List(pair("A"), pair("B")), List(pair("A"))) == Set("B"))

private def findsTranslationMismatches(): Unit =
  assert(ContentChecks.translationMismatches(List(pair("A")), List(pair("A", theme = "cloud"))) == List("A"))

private def validContentHasNoProblem(): Unit =
  val report = Report.build(twelvePairs, twelvePairs, icons)
  assert(report.isValid, report.problems)
