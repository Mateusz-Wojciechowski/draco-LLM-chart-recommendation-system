from draco import schema_from_dataframe, dict_to_facts
import json


def generate_dataframe_facts_schema(dataframe):
    """
        Generate a facts schema (list of ASP facts) from a given pandas DataFrame
        using Draco's fact generation utilities.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            The input dataframe from which to generate the facts schema.

        Returns
        -------
        list of str
            A list of ASP facts (strings) representing the schema of the given dataframe.
    """

    dataframe_schema = schema_from_dataframe(dataframe)
    dataframe_facts_schema = dict_to_facts(dataframe_schema)
    return dataframe_facts_schema


def clean_char_spec(spec_str):

    """
        Clean a Vega-Lite chart specification by removing 'data' and 'datasets' fields.

        Parameters
        ----------
        spec_str : str
            A JSON string representing a Vega-Lite chart specification.

        Returns
        -------
        str
            The cleaned chart specification as a JSON-formatted string, without 'data' and 'datasets' fields.
        """

    spec = json.loads(spec_str)
    if 'data' in spec:
        del spec['data']
    if 'datasets' in spec:
        del spec['datasets']

    return json.dumps(spec, ensure_ascii=False, indent=2)