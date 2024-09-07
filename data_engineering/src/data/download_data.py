import sys
from utils.data import download_dataset

def main(dataset_key: str) -> None:
    """
    Main function to download a dataset based on the key provided.
    
    Args:
        dataset_key (str): The key for the dataset to be downloaded, which should be in the DATASETS dictionary.
    """
    download_dataset(dataset_key)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python get_dvc_dataset.py <dataset_key>")
        sys.exit(1)
    
    dataset_key = sys.argv[1]
    main(dataset_key)