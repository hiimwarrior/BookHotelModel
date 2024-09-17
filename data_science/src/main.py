import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='Run machine learning experiments.')
    parser.add_argument('experiment', type=str, help='The experiment to run (e.g., random_forest)')
    parser.add_argument('--data', type=str, required=True, help='Version of the dataset')
    parser.add_argument('--version', type=str, required=True, help='Version of the model')
    
    args = parser.parse_args()

    if args.experiment == 'random_forest':
        from modelling.hotel_booking.random_forest.v1 import run_random_forest_experiment
        run_random_forest_experiment(args.data, args.version)
    if args.experiment == 'xgboost':
        from modelling.hotel_booking.xgboost.v1 import run_xgboost_experiment
        run_xgboost_experiment(args.data, args.version)
    else:
        print(f"Unknown experiment: {args.experiment}")
        sys.exit(1)

if __name__ == "__main__":
    main()
