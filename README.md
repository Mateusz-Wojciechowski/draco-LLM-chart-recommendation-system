# Chart recommendation system using Draco evaluated by Draco constraints and a modified Lida evaluator

## NOTE
This repository relies on a forked version of the Lida library available here: https://github.com/Mateusz-Wojciechowski/lida-for-vega-lite

To use this modified version in your virtual environment, run:
 
```
pip install git+https://github.com/Mateusz-Wojciechowski/lida-for-vega-lite
```
To view the report in an interactive form (working links etc.) it must be downloaded as the basic view in github repository doesn't provide this functionality
## Repository description


This repository contains a visualization recommendation system. It starts by utilizing an LLM to select a pair of columns that it believes will yield the most meaningful visualization. For each possible column pair including the pair selected by the LLM, the system generates a chart specification in a format understandable by Draco.

Draco then produces top-1, top-3, and top-5 chart recommendations for each column pair. The recommendations are assigned scores based on Lida (a forked version of the library) and Draco cost. These scores are combined into a final overall score.

## A brief code overview
The primary function is located in run_recommendation_system.py. By following the steps within the main function, and examining the functions it calls, you can fully understand the implementation flow.
Each function includes a docstring that explains its parameters, return values, and functionality.
The code is split into separate folders according to its purpose (e.g., LLM column selection, Draco chart generation, evaluation scoring, etc.). Refer to these folders for more details on each module's responsibilities.


