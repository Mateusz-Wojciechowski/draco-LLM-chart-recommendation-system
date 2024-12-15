import draco as draco
import altair as alt
from IPython.display import display
from visualization.schema_preparation import clean_char_spec


def recommend_charts(spec, drc, renderer, data, num=5, labeler=lambda i: f"CHART {i+1}"):
    """
        Generate chart recommendations from a given Draco specification using the provided renderer and data.

        Parameters
        ----------
        spec : list of str
            The ASP facts representing a partial visualization specification.
        drc : draco.Draco
            An instance of Draco used to complete specifications.
        renderer : draco.renderer.BaseRenderer
            A renderer to produce visualization objects from specifications.
        data : pandas.DataFrame
            The dataset to render.
        num : int, optional
            The number of recommendations to produce, by default 5.
        labeler : callable, optional
            A function that given an index returns a chart name, by default lambda i: f"CHART {i+1}".

        Returns
        -------
        list of dict
            A list of dictionaries, each containing 'name', 'specification', and 'cost'
            corresponding to each recommended chart.
    """

    charts = []
    for i, model in enumerate(drc.complete_spec(spec, num)):
        chart_name = labeler(i)
        spec = draco.answer_set_to_dict(model.answer_set)

        chart = renderer.render(spec=spec, data=data)

        if isinstance(chart, alt.FacetChart) and chart.facet.column is not alt.Undefined:
            chart = chart.configure_view(continuousWidth=130, continuousHeight=130)

        chart = chart.to_json()
        chart = clean_char_spec(chart)
        charts.append({'name': chart_name, 'specification': chart, 'cost': model.cost[0]})

    return charts


def generate_input_spec_two_columns(facts_schema, column1, column2):
    """
        Generate an ASP specification input by adding encoding facts for two selected columns.

        Parameters
        ----------
        facts_schema : list of str
            The facts schema representing the dataset fields and statistics.
        column1 : str
            The first column name to encode.
        column2 : str
            The second column name to encode.

        Returns
        -------
        list of str
            The combined specification including the provided fields encoded.
    """

    input_spec_base = facts_schema + [
        "entity(view,root,v0).",
        "entity(mark,v0,m0).",
    ]

    input_spec = input_spec_base + [
        "entity(encoding,m0,e0).",
        f"attribute((encoding,field),e0,{column1}).",
        "entity(encoding,m0,e1).",
        f"attribute((encoding,field),e1,{column2}).",
    ]

    return input_spec