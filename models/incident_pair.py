
from models.card import IncidentCard, SolutionCard


class IncidentPair:
    """Represents a valid incident-solution pair."""

    def __init__(
        self,
        incident: IncidentCard,
        solution: SolutionCard
    ):
        if not isinstance(incident, IncidentCard):
            raise TypeError("incident must be an IncidentCard.")

        if not isinstance(solution, SolutionCard):
            raise TypeError("solution must be a SolutionCard.")

        if not incident.matches(solution):
            raise ValueError(
                "The incident and solution do not belong to the same pair."
            )

        self.incident = incident
        self.solution = solution

    @property
    def pair_id(self) -> str:
        """Returns the identifier shared by both cards."""
        return self.incident.pair_id

    def is_matched(self) -> bool:
        """Checks whether both cards have been matched."""
        return (
            self.incident.is_matched()
            and self.solution.is_matched()
        )

    def mark_as_matched(self):
        """Marks both cards as successfully matched."""
        self.incident.mark_as_matched()
        self.solution.mark_as_matched()

    def get_cards(self) -> tuple:
        """Returns the two cards forming the pair."""
        return self.incident, self.solution