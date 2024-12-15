from lida import Manager, llm, TextGenerationConfig
from lida.datamodel import Goal
from utils.openai_api_key import API_KEY


def evaluate_chart(code):
    """
        Evaluate a given Altair chart specification using LIDA's evaluation capabilities.

        Parameters
        ----------
        code : str
            The Vega-Lite chart specification to be evaluated.

        Returns
        -------
        float
            The mean score assigned by LIDA across various evaluation dimensions.
    """
    lida = Manager(text_gen=llm("openai", api_key=API_KEY))
    textgen_config = TextGenerationConfig(n=1, temperature=0, use_cache=True)

    goal = Goal(question="", visualization="", rationale="")

    evaluations = lida.evaluate(code=code, goal=goal, textgen_config=textgen_config)[0]

    score = 0
    for evaluation in evaluations:
        score += evaluation["score"]

    return score/len(evaluations)