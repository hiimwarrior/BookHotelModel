from abc import ABC, abstractmethod

class BaseStorage(ABC):
    """Base class for storage clients like S3, GCP, Azure."""

    @abstractmethod
    def download_model(self, cloud_key, local_file_path):
        """Download a model from cloud storage."""
        pass