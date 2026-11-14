
class CountdownTimer:
    """Countdown that never reads the system clock.

    The caller (the Pygame loop, or a test) tells it how much time has
    passed with tick(). This makes the timer fully predictable in tests.
    """

    def __init__(self, time_limit: float):
        if time_limit <= 0:
            raise ValueError("The time limit must be positive.")

        self._remaining = float(time_limit)
        self._running = True

    @property
    def remaining(self) -> float:
        """Seconds left (never below zero)."""
        return self._remaining

    def is_running(self) -> bool:
        return self._running

    def is_expired(self) -> bool:
        return self._remaining <= 0

    def tick(self, delta_seconds: float):
        """Removes the elapsed time from the countdown."""
        if delta_seconds < 0:
            raise ValueError("Elapsed time cannot be negative.")

        self._change_by(-delta_seconds)

    def add(self, seconds: float):
        """Adds (bonus) or removes (penalty) time, e.g. from a special card."""
        self._change_by(seconds)

    def stop(self):
        """Freezes the countdown at the end of the game."""
        self._running = False

    def _change_by(self, seconds: float):
        if self._running:
            self._remaining = max(0.0, self._remaining + seconds)
