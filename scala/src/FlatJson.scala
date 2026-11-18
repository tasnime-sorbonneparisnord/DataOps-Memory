package dataops.quality

/** Lecteur JSON minimal pour le format de `data/incidents*.json` :
  * une liste d'objets dont toutes les valeurs sont du texte.
  *
  * Il ne dépend d'aucune bibliothèque. Toute autre forme de JSON est refusée
  * avec un message clair (Left) plutôt qu'une exception.
  */
object FlatJson:

  type Record = Map[String, String]

  def parseRecords(text: String): Either[String, List[Record]] =
    val reader = Reader(text)
    for
      records <- reader.readArray()
      _ <- reader.expectEnd()
    yield records

  /** Curseur de lecture : seul endroit du programme avec un état modifiable (la position). */
  private final class Reader(text: String):
    private var position = 0

    def readArray(): Either[String, List[Record]] =
      expect('[').flatMap { _ =>
        if peekIs(']') then
          advance()
          Right(Nil)
        else readSeparated(readObject(), ']')
      }

    def expectEnd(): Either[String, Unit] =
      skipSpaces()
      if position == text.length then Right(())
      else Left(error("fin du fichier attendue"))

    private def readObject(): Either[String, Record] =
      expect('{').flatMap { _ =>
        if peekIs('}') then
          advance()
          Right(Map.empty)
        else readSeparated(readField(), '}').map(_.toMap)
      }

    private def readField(): Either[String, (String, String)] =
      for
        key <- readString()
        _ <- expect(':')
        value <- readString()
      yield key -> value

    /** Lit « élément (, élément)* fermeture » et renvoie la liste des éléments. */
    private def readSeparated[A](readItem: => Either[String, A], closing: Char): Either[String, List[A]] =
      @annotation.tailrec
      def loop(items: List[A]): Either[String, List[A]] =
        readItem match
          case Left(message) => Left(message)
          case Right(item) =>
            skipSpaces()
            current match
              case Some(',') => advance(); loop(item :: items)
              case Some(`closing`) => advance(); Right((item :: items).reverse)
              case _ => Left(error(s"',' ou '$closing' attendu"))
      loop(Nil)

    private def readString(): Either[String, String] =
      expect('"').flatMap { _ =>
        val builder = StringBuilder()
        @annotation.tailrec
        def loop(): Either[String, String] =
          current match
            case None => Left(error("texte non terminé"))
            case Some('"') => advance(); Right(builder.toString)
            case Some('\\') => advance(); readEscape(builder) match
                case Left(message) => Left(message)
                case Right(_) => loop()
            case Some(character) => builder += character; advance(); loop()
        loop()
      }

    private def readEscape(builder: StringBuilder): Either[String, Unit] =
      val simpleEscapes = Map('"' -> '"', '\\' -> '\\', '/' -> '/', 'n' -> '\n', 't' -> '\t', 'r' -> '\r')
      current match
        case Some('u') if position + 4 < text.length =>
          val hex = text.substring(position + 1, position + 5)
          position += 5
          hex.toIntOption(16) match
            case Some(code) => builder += code.toChar; Right(())
            case None => Left(error(s"code \\u$hex invalide"))
        case Some(letter) if simpleEscapes.contains(letter) =>
          builder += simpleEscapes(letter); advance(); Right(())
        case _ => Left(error("échappement invalide"))

    private def expect(expected: Char): Either[String, Unit] =
      skipSpaces()
      if current.contains(expected) then
        advance()
        Right(())
      else Left(error(s"'$expected' attendu"))

    private def peekIs(character: Char): Boolean =
      skipSpaces()
      current.contains(character)

    private def current: Option[Char] = text.lift(position)
    private def advance(): Unit = position += 1
    private def skipSpaces(): Unit = while current.exists(_.isWhitespace) do advance()
    private def error(message: String): String = s"JSON invalide (position $position) : $message"

  extension (text: String)
    private def toIntOption(radix: Int): Option[Int] =
      try Some(Integer.parseInt(text, radix))
      catch case _: NumberFormatException => None
