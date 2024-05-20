class DataFillingError(Exception):
    """Exception raised for errors in the input data."""

    def __init__(self, message="Error occurred during data filling"):
        self.message = message
        super().__init__(self.message)