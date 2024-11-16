# app/auth/exceptions.py

import logging


class RedirectToLoginException(Exception):
    """
    Custom exception to trigger redirection to the login page.
    Includes the URL that triggered the exception for redirecting after login.
    """
    def __init__(self, original_url: str):
        super().__init__(f"Redirect to login triggered by URL: {original_url}")
        self.original_url = original_url
        logging.debug(f"RedirectToLoginException: {original_url}")