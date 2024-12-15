from draco import Draco
from draco.renderer import AltairRenderer
from visualization.schema_preparation import generate_dataframe_facts_schema
from vega_datasets import data
from visualization.column_selection import choose_columns_for_visualization
from evaluation.chart_scoring import score_and_save_recommendations
from utils.config import OUTPUT_FILES_PATHS, RECOMMENDATION_AMOUNT_LIST
from evaluation.generate_result_table import create_result_table


def main():
    """
        Main entry point for the visualization recommendation evaluation process.

        Steps:
        1. Load a sample dataset.
        2. Generate facts schema using Draco.
        3. Let the LLM choose two columns for visualization.
        4. Generate recommendations for those columns and for all other column pairs.
        5. Evaluate each recommendation using both LIDA and Draco scores.
        6. Save the results in CSV files.
    """

    dataframe = data.seattle_weather()
    dataframe_columns = list(dataframe.columns.values)
    print(dataframe_columns)

    dataframe_facts_schema = generate_dataframe_facts_schema(dataframe)
    drc = Draco()
    renderer = AltairRenderer()

    selected_columns, remaining_column_pairs = choose_columns_for_visualization(dataframe_columns)
    print("Column names:", selected_columns)
    print("Other column pairs:", remaining_column_pairs)

    for how_many_recommendations, output_file_path in zip(RECOMMENDATION_AMOUNT_LIST, OUTPUT_FILES_PATHS):
        score_and_save_recommendations(selected_columns, remaining_column_pairs, output_file_path, dataframe_facts_schema, drc, renderer, dataframe, how_many_recommendations)

    create_result_table(OUTPUT_FILES_PATHS, 'scoring_results/result_table.csv')

if __name__ == '__main__':
    main()