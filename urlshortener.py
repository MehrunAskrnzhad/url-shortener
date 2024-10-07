import os
import json
import random
import string
from urllib.parse import urlparse


class URLShortener:
    """URL shortener class that generates shortcodes for URLs."""

    class InvalidURLError(Exception):
        """Exception raised for invalid URLs."""
        pass

    class InvalidDatabaseError(Exception):
        """Exception raised for invalid database files."""
        pass

    class URLNotFoundError(Exception):
        """Exception raised when the shortcode is not found in the database."""
        pass

    def __init__(self, database_file: str, website_url: str) -> None:
        """
        Initialize the URLShortener instance.

        Args:
            database_file: Path to the database file.
            website_url: Base URL of the shortened URLs.

        Raises:
            FileNotFoundError: If the database file does not exist.
        """
        self.database_file: str = (
            database_file if os.path.exists(database_file) and os.path.isfile(database_file) else None
        )
        if self.database_file is None:
            raise FileNotFoundError('Database file does not exist.')

        self.website_url: str = self.validate_url(website_url)
        self.data: dict[str, str] = self.load_database()

    def validate_url(self, url: str) -> str:
        """
        Validate the URL format.

        Args:
            url: The URL to validate.

        Returns:
            The validated URL.

        Raises:
            InvalidURLError: If the URL is not valid.
        """
        parsed_url = urlparse(url)
        if parsed_url.scheme and parsed_url.netloc:
            if not parsed_url.path.endswith('/'):
                url += '/'
            return url
        raise self.InvalidURLError(f"URL {url} is not valid.")

    def load_database(self) -> dict[str, str]:
        """
        Load the data from the database file.

        Returns:
            The loaded data.

        Raises:
            InvalidDatabaseError: If the database file does not contain JSON data.
        """
        try:
            with open(self.database_file) as file:
                data = file.read()
                if not data :
                    data = {}
                else :
                    data = json.loads(data)
        except json.JSONDecodeError:
            raise self.InvalidDatabaseError(f"Database file {self.database_file} does not contain JSON data.")
        self.data = data
        self.save_database()
        return data
    def save_database(self) -> None:
        """
        Save the data to the database file.

        Raises:
            InvalidDatabaseError: If failed to save the database file.
        """
        try:
            with open(self.database_file, 'w') as file:
                json.dump(self.data, file, indent=4)
        except Exception:
            raise self.InvalidDatabaseError(f"Failed to save database file {self.database_file}.")

    def shorten_url(self, url: str) -> str:
        """
        Shorten the given URL by generating a shortcode.

        Args:
            url: The URL to be shortened.

        Returns:
            The shortened URL.

        Raises:
            InvalidDatabaseError: If failed to save the database file.
        """
        shortcode = self.generate_shortcode()
        self.data[shortcode] = url
        self.save_database()
        return self.website_url + shortcode

    def generate_shortcode(self, length: int = 6) -> str:
        """
        Generate a unique shortcode.

        Args:
            length: Length of the shortcode. Defaults to 6.

        Returns:
            The generated shortcode.
        """
        self.load_database()
        existing_codes = self.data.keys()
        shortcode = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
        while shortcode in existing_codes:
            shortcode = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
        return shortcode

    def get_original_url(self, shortcode: str) -> str | None:
        """
        Get the original URL associated with the given shortcode.

        Args:
            shortcode: The shortcode to retrieve the original URL.

        Returns:
            The original URL if found, None otherwise.
        """
        self.load_database()
        return self.data.get(shortcode)

    def is_shortened_url(self, url: str) -> bool:
        """
        Checks if the given URL is already shortened.

        Args:
            url: The URL to check.

        Returns:
            bool: True if the URL is already shortened, False otherwise.
        """
        return url in self.data.values()

    def get_shortened_url(self, url: str) -> str | None:
        """
        Get the shortened URL associated with the given original URL.

        Args:
            url: The original URL to retrieve the shortened URL.

        Returns:
            The shortened URL if found, None otherwise.
        """
        shortcode = next((shortcode for shortcode, original_url in self.data.items() if original_url == url), None)
        if shortcode is not None:
            return self.website_url + shortcode
        return None
