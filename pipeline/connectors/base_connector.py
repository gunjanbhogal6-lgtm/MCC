"""
Base connector class for all API integrations
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from ..utils.logger import get_logger


class BaseConnector(ABC):
    """Base class for all API connectors"""
    
    def __init__(self):
        self.logger = get_logger()
        self.is_authenticated = False
        self.name = self.__class__.__name__
    
    @abstractmethod
    def authenticate(self) -> bool:
        """
        Authenticate with the service.
        
        Returns:
            True if authentication successful, False otherwise
        """
        pass
    
    def logout(self) -> bool:
        """
        Logout from the service.
        
        Returns:
            True if logout successful
        """
        self.is_authenticated = False
        return True
    
    def health_check(self) -> Dict:
        """
        Check if the connector is healthy.
        
        Returns:
            Health status dictionary
        """
        return {
            "connector": self.name,
            "authenticated": self.is_authenticated,
            "status": "healthy" if self.is_authenticated else "disconnected"
        }
    
    def get_rate_limit_info(self) -> Dict:
        """
        Get rate limit information for the service.
        
        Returns:
            Dictionary with rate limit details
        """
        return {
            "connector": self.name,
            "rate_limit": "not_implemented",
            "remaining": None,
            "reset": None
        }
    
    def __enter__(self):
        """Context manager entry"""
        self.authenticate()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.logout()
        return False