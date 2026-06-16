class ContextWindow:
    """
    Handles context size budgeting.

    V1:
    Character-based budgeting.

    Future:
    Token-based budgeting.
    """

    def __init__(
        self,
        max_characters: int = 15000,
    ):
        self.max_characters = max_characters

    def fits(
        self,
        current_size: int,
        text: str,
    ) -> bool:

        return current_size + len(text) <= self.max_characters

    def remaining(
        self,
        current_size: int,
    ) -> int:

        return max(
            0,
            self.max_characters - current_size,
        )
    
    def token_budget(self) -> int:
        """
        Placeholder for future token-based budgeting.
        """
        raise NotImplementedError("Token-based budgeting not implemented yet.")
