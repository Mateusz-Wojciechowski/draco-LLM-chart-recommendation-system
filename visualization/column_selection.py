from openai import OpenAI
from itertools import combinations
from dotenv import load_dotenv
import os
from utils.openai_api_key import API_KEY



def create_possible_column_pairs(columns, picked_pair):
    """
       Create a list of all possible column pairs except the one selected by the LLM.

       Parameters
       ----------
       columns : list[str]
           A list of column names from the dataset.
       picked_pair : list[str]
           The pair of columns chosen by the LLM.

       Returns
       -------
       list[list[str]]
           A list of column pairs, each represented as a two-element list, excluding the chosen pair.
    """

    all_pairs = list(combinations(columns, 2))
    remaining_pairs = [list(pair) for pair in all_pairs if set(pair) != set(picked_pair)]
    return remaining_pairs


def choose_columns_for_visualization(columns):
    """
        Use the LLM via the OpenAI API to select two columns that would be most suitable for creating a meaningful
        visualization from the given dataset.

        Parameters
        ----------
        columns : list[str]
            A list of column names from the dataset.

        Returns
        -------
        tuple
            A tuple containing:
            - selected_columns (list[str]): The two columns selected by the LLM.
            - remaining_pairs (list[list[str]]): A list of other possible column pairs.
    """

    client = OpenAI(
        api_key=API_KEY)

    prompt = (
        "You are a data visualization expert. Given the following list of columns in a dataset and their types, "
        "select two columns that are the most suitable for creating a meaningful visualization. "
        "Respond only with the names of the two selected columns, separated by a comma. "
        "Here is the list of columns:\n\n"
    )
    for col_name in columns:
        prompt += f"- {col_name}\n"

    prompt += "\nPlease return only the two selected column names, separated by a comma."

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for data analysis."},
            {"role": "user", "content": prompt}
        ]
    )

    output = response.choices[0].message.content
    selected_columns = [col.strip() for col in output.split(",")]
    remaining_pairs = create_possible_column_pairs(columns, selected_columns)

    return selected_columns, remaining_pairs
