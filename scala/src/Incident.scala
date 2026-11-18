package dataops.quality

/** Une paire incident / solution telle qu'écrite dans `data/incidents*.json`. Immuable. */
final case class Incident(
    pairId: String,
    theme: String,
    incident: String,
    solution: String,
    explanation: String,
    incidentIcon: String,
    solutionIcon: String
):
  def labels: List[String] = List(incident, solution)
  def icons: List[String] = List(incidentIcon, solutionIcon)

object Incident:

  val RequiredFields: List[String] = List("pair_id", "theme", "incident", "solution", "explanation")

  /** Construit un Incident, ou explique pourquoi c'est impossible (champ manquant ou vide). */
  def fromRecord(record: FlatJson.Record, position: Int): Either[String, Incident] =
    val missing = RequiredFields.filter(field => record.get(field).forall(_.isBlank))
    if missing.nonEmpty then Left(s"Paire n°${position + 1} : champ(s) manquant(s) ${missing.mkString(", ")}")
    else
      Right(Incident(
        pairId = record("pair_id"),
        theme = record("theme"),
        incident = record("incident"),
        solution = record("solution"),
        explanation = record("explanation"),
        incidentIcon = record.getOrElse("incident_icon", ""),
        solutionIcon = record.getOrElse("solution_icon", "")
      ))

  /** Toutes les paires valides, ou la liste de toutes les erreurs trouvées (pas seulement la première). */
  def fromRecords(records: List[FlatJson.Record]): Either[List[String], List[Incident]] =
    val results = records.zipWithIndex.map((record, position) => fromRecord(record, position))
    val errors = results.collect { case Left(message) => message }
    if errors.nonEmpty then Left(errors) else Right(results.collect { case Right(incident) => incident })
