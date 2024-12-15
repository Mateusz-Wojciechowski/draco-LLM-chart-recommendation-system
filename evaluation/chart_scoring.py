from visualization.chart_generation import generate_input_spec_two_columns, recommend_charts
from evaluation.lida_evaluation import evaluate_chart
import csv
from utils.config import RESULT_CSV_COLUMNS


def calculate_chart_scores(column_pair, dataframe_facts_schema, drc, renderer, dataframe, how_many):
    """
        Calculate the average LIDA and Draco scores for charts generated from a specific column pair.

        Parameters
        ----------
        column_pair : list of str
            The pair of columns used for visualization.
        dataframe_facts_schema : list of str
            The facts schema from the dataset.
        drc : draco.Draco
            An instance of Draco.
        renderer : draco.renderer.BaseRenderer
            An instance of the AltairRenderer.
        dataframe : pandas.DataFrame
            The dataset to visualize.
        how_many : int
            The number of chart recommendations to generate.

        Returns
        -------
        tuple
            A tuple containing (mean_draco_score, mean_lida_score, final_score).
    """

    input_spec = generate_input_spec_two_columns(dataframe_facts_schema, column_pair[0], column_pair[1])
    selected_columns_recommendations = recommend_charts(input_spec, drc, renderer, dataframe, how_many)

    mean_draco_score = 0
    mean_lida_score = 0
    for recommendation in selected_columns_recommendations:
        mean_draco_score += recommendation['cost']
        mean_lida_score += evaluate_chart(recommendation['specification'])

    mean_draco_score = mean_draco_score / len(selected_columns_recommendations)
    mean_lida_score = mean_lida_score / len(selected_columns_recommendations)
    final_score = normalize_score(mean_lida_score, mean_draco_score)

    return mean_draco_score, mean_lida_score, final_score


def normalize_score(lida_score, draco_score):
    """
        Normalize and combine LIDA and Draco scores into a single final score.

        Parameters
        ----------
        lida_score : float
            The average LIDA score (1-10).
        draco_score : float
            The average Draco cost score (lower is better).

        Returns
        -------
        float
            A combined score where both LIDA and Draco are normalized and averaged.
    """

    normalized_lida_score = lida_score / 10
    normalized_draco_score = 1.0/(1.0 + draco_score)
    final_score = (normalized_lida_score + normalized_draco_score) / 2.0
    return final_score


def score_and_save_recommendations(selected_columns, remaining_column_pairs, output_csv_path, dataframe_facts_schema, drc, renderer, dataframe, how_many_recommendations):
    """
        Generate scores for LLM-selected columns and all remaining column pairs, and save the results to a CSV file.

        Parameters
        ----------
        selected_columns : list of str
            The pair of columns chosen by the LLM.
        remaining_column_pairs : list of list of str
            Other pairs of columns not chosen by the LLM.
        output_csv_path : str
            The path to the CSV file where results should be saved.
        dataframe_facts_schema : list of str
            The facts schema for the dataset.
        drc : draco.Draco
            Draco instance for specification completion.
        renderer : draco.renderer.BaseRenderer
            Renderer instance (AltairRenderer) for chart rendering.
        dataframe : pandas.DataFrame
            The dataset to visualize.
        how_many_recommendations : int
            The number of chart recommendations to generate for each column pair.
    """

    with open(output_csv_path, 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(RESULT_CSV_COLUMNS)

        draco_score, lida_score, final_score = calculate_chart_scores(selected_columns, dataframe_facts_schema, drc,
                                                                      renderer, dataframe, how_many_recommendations)
        writer.writerow([selected_columns[0], selected_columns[1], how_many_recommendations, lida_score, draco_score, final_score, True])

        for column_pair in remaining_column_pairs:
            draco_score, lida_score, final_score = calculate_chart_scores(column_pair, dataframe_facts_schema, drc,
                                                                          renderer, dataframe, how_many_recommendations)
            writer.writerow([column_pair[0], column_pair[1], how_many_recommendations, lida_score, draco_score, final_score, False])


