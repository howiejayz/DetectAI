import argparse
import pandas as pd

def concat_and_shuffle_csv(files, output):
    dfs = [pd.read_csv(file) for file in files]
    combined_df = pd.concat(dfs, ignore_index=True)
    shuffled_df = combined_df.sample(frac=1).reset_index(drop=True)
    shuffled_df.to_csv(output, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Concatenate and shuffle multiple CSV files.")
    parser.add_argument('--files', nargs='+', required=True, help='List of CSV files to concatenate.')
    parser.add_argument('--output', default='combined_dataset.csv', help='Path to save the concatenated and shuffled dataset.')

    args = parser.parse_args()

    concat_and_shuffle_csv(args.files, args.output)
