import pandas as pd
from unittest import mock
from src.modelling.hotel_booking.random_forest.v1 import run_random_forest_experiment

def test_run_random_forest_experiment(mocker):
    # Mock setup_mlflow_experiment to avoid actual MLflow calls
    mocker.patch('src.modelling.hotel_booking.random_forest.v1', return_value=None)
    
    # Mock MLflow functions
    mock_mlflow_start_run = mocker.patch('mlflow.start_run')
    mock_mlflow_log_param = mocker.patch('mlflow.log_param')
    mock_mlflow_log_metric = mocker.patch('mlflow.log_metric')
    mock_mlflow_sklearn_log_model = mocker.patch('mlflow.sklearn.log_model')
    mock_mlflow_register_model = mocker.patch('mlflow.register_model')
    
    # Mock os.path.exists to pretend the file exists
    mocker.patch('os.path.exists', return_value=True)
    
    # Mock pandas read_csv to return a sample dataframe
    sample_df = pd.DataFrame({
        'feature1': [1, 2, 3],
        'feature2': [4, 5, 6],
        'is_canceled': [0, 1, 0]
    })
    mocker.patch('pandas.read_csv', return_value=sample_df)
    
    # Mock save_model to avoid actual file saving
    mock_save_model = mocker.patch('utils.models.save_model', return_value=None)
    
    # Call the function
    run_random_forest_experiment('1.0', '1.0')
    
    # Assert that MLflow functions were called correctly
    mock_mlflow_start_run.assert_called_once()
    mock_mlflow_log_param.assert_called_with('n_estimators', 100)
    
    # Check if MLflow logging functions were called
    assert mock_mlflow_log_metric.call_count == 5  # There are 5 metrics to log
    assert mock_mlflow_sklearn_log_model.called
    assert mock_mlflow_register_model.called
    assert mock_save_model.called

    # You may add more specific assertions based on what you expect
