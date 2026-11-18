package dataops.quality

/** Règles de qualité du contenu du jeu, écrites comme des fonctions pures :
  * mêmes entrées → même résultat, aucun fichier lu ou écrit ici.
  */
object ContentChecks:

  /** Au-delà, le texte risque de ne plus tenir sur une carte du jeu. */
  val MaxLabelLength = 32
  /** Le jeu tire jusqu'à 12 paires (niveau Difficile) : il en faut au moins autant. */
  val MinimumPairs = 12

  def duplicatePairIds(incidents: List[Incident]): Set[String] =
    incidents.groupBy(_.pairId).collect { case (id, copies) if copies.size > 1 => id }.toSet

  def pairsByTheme(incidents: List[Incident]): Map[String, Int] =
    incidents.groupBy(_.theme).view.mapValues(_.size).toMap

  def labelsTooLong(incidents: List[Incident], maxLength: Int = MaxLabelLength): List[String] =
    incidents.flatMap(_.labels).filter(_.length > maxLength)

  def missingIcons(incidents: List[Incident], availableIcons: Set[String]): Set[String] =
    incidents.flatMap(_.icons).filter(_.nonEmpty).toSet -- availableIcons

  /** Paires présentes dans une langue mais pas dans l'autre. */
  def translationGaps(french: List[Incident], english: List[Incident]): Set[String] =
    val frenchIds = french.map(_.pairId).toSet
    val englishIds = english.map(_.pairId).toSet
    (frenchIds diff englishIds) union (englishIds diff frenchIds)

  /** Une même paire doit garder son thème et ses icônes dans les deux langues. */
  def translationMismatches(french: List[Incident], english: List[Incident]): List[String] =
    val englishById = english.map(incident => incident.pairId -> incident).toMap
    french.flatMap { frenchPair =>
      englishById.get(frenchPair.pairId).collect {
        case englishPair if englishPair.theme != frenchPair.theme || englishPair.icons != frenchPair.icons =>
          frenchPair.pairId
      }
    }

  /** Tous les contrôles d'une langue, regroupés en une liste de problèmes (vide = tout va bien). */
  def problemsFor(language: String, incidents: List[Incident], availableIcons: Set[String]): List[String] =
    val tooFew =
      if incidents.size < MinimumPairs then List(s"seulement ${incidents.size} paires (minimum $MinimumPairs)")
      else Nil
    val messages =
      tooFew ++
        duplicatePairIds(incidents).toList.sorted.map(id => s"pair_id en double : $id") ++
        labelsTooLong(incidents).map(label => s"texte trop long pour une carte : « $label »") ++
        missingIcons(incidents, availableIcons).toList.sorted.map(icon => s"icône introuvable : $icon")
    messages.map(message => s"[$language] $message")

  def translationProblems(french: List[Incident], english: List[Incident]): List[String] =
    translationGaps(french, english).toList.sorted.map(id => s"[fr/en] paire absente d'une des langues : $id") ++
      translationMismatches(french, english).map(id => s"[fr/en] thème ou icônes différents : $id")
