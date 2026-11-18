package dataops.quality

/** Résultat du contrôle : quelques chiffres et la liste des problèmes trouvés. */
final case class Report(
    frenchPairs: Int,
    englishPairs: Int,
    pairsByTheme: Map[String, Int],
    problems: List[String]
):
  def isValid: Boolean = problems.isEmpty

  def render: String =
    val themes = pairsByTheme.toList.sortBy(_._1).map((theme, count) => f"  - $theme%-10s $count paires")
    val verdict =
      if isValid then List("Résultat : OK, aucun problème trouvé.")
      else s"Résultat : ${problems.size} problème(s)" :: problems.map(problem => s"  * $problem")
    (List(
      "=== Contrôle qualité des incidents DataOps Memory ===",
      s"Paires : $frenchPairs en français, $englishPairs en anglais",
      "Paires par thème :"
    ) ++ themes ++ verdict).mkString("\n")

object Report:
  def build(french: List[Incident], english: List[Incident], availableIcons: Set[String]): Report =
    Report(
      frenchPairs = french.size,
      englishPairs = english.size,
      pairsByTheme = ContentChecks.pairsByTheme(french),
      problems = ContentChecks.problemsFor("fr", french, availableIcons) ++
        ContentChecks.problemsFor("en", english, availableIcons) ++
        ContentChecks.translationProblems(french, english)
    )
