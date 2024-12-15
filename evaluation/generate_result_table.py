import pandas as pd
from utils.config import OUTPUT_FILES_PATHS

def create_result_table(input_files, output_file):
    """
    Summarizes and consolidates results from multiple CSV files into a single output CSV file.

    This function iterates over a list of CSV files, verifies the presence of specific columns,
    and extracts key metrics. For each CSV file, it identifies:

      • The `chart_count` associated with the dataset.
      • The `final_score_selected_pair`: The final score for the pair of columns chosen by the LLM (if present).
      • The `highest_scoring_column_pair`: The pair of columns that yields the highest `final_score`.
      • The `highest_final_score`: The maximum `final_score` found in that CSV.

    After collecting these metrics for each input file, the function writes the consolidated information
    to a new CSV specified by `output_file`.

    Parameters
    ----------
    input_files : List[str]
        A list of file paths for the input CSV files. Each file should contain the following columns:
        ['col1', 'col2', 'chart_count', 'lida_score', 'draco_cost', 'final_score', 'llm_selected'].
    output_file : str
        The file path where the summarized results will be saved as a CSV.

    Returns
    -------
    None
        This function does not return a value. It writes the consolidated results directly to `output_file`.
    """
    output_data = []

    for file in input_files:
        try:
            df = pd.read_csv(file)
            required_columns = ['col1', 'col2', 'chart_count', 'lida_score', 'draco_cost', 'final_score', 'llm_selected']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                print(f"File {file} skipped, missing columns: {missing_columns}")
                continue

            chart_count = df['chart_count'].iloc[0]

            selected_rows = df[df['llm_selected'] == True]
            if not selected_rows.empty:
                selected_row = selected_rows.iloc[0]
                final_score_selected = selected_row['final_score']
            else:
                final_score_selected = pd.NA

            if not df.empty:
                max_score_row = df.loc[df['final_score'].idxmax()]
                highest_scoring_column_pair = f"{max_score_row['col1']},{max_score_row['col2']}"
                highest_final_score = max_score_row['final_score']
            else:
                highest_scoring_column_pair = pd.NA
                highest_final_score = pd.NA

            output_data.append({
                'chart_count': chart_count,
                'final_score_selected_pair': final_score_selected,
                'highest_scoring_column_pair': highest_scoring_column_pair,
                'highest_final_score': highest_final_score
            })

            print(f"Successfully processed file: {file}")

        except Exception as e:
            print(f"Error processing file {file}: {e}")
            continue

    if output_data:
        output_df = pd.DataFrame(output_data)

        output_df = output_df[['chart_count', 'final_score_selected_pair', 'highest_scoring_column_pair', 'highest_final_score']]

        output_df.to_csv(output_file, index=False)
        print(f"Output file saved as {output_file}")
    else:
        print("No data to save")
