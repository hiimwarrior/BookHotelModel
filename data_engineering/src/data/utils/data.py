import requests
from utils.config import DATASETS
import os

def download_dataset(dataset_key: str) -> None:
    """
    Download a dataset based on the key provided in the configuration.

    Args:
        dataset_key (str): The key for the dataset to be downloaded, which should be in the DATASETS dictionary.
    """
    if dataset_key not in DATASETS:
        raise ValueError(f"Dataset '{dataset_key}' not found in configuration.")
    
    dataset = DATASETS[dataset_key]
    url = dataset['url']
    output_path = dataset['destination']
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Crear el directorio si no existe
            output_dir = os.path.dirname(output_path)
            if output_dir:  # Verifica si output_path contiene un directorio
                os.makedirs(output_dir, exist_ok=True)

            with open(output_path, 'wb') as file:
                file.write(response.content)
            print(f"Data downloaded and saved in {output_path}")
            # Obtener la ruta completa del archivo
            absolute_path = os.path.abspath(output_path)
            print(f'Data downloaded and saved in: {absolute_path}')
        else:
            raise Exception(f"Failed to download data. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        raise
