import random

import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State, no_update

from algorithms.bubble_sort import bubble_sort
from algorithms.selection_sort import selection_sort
from algorithms.insertion_sort import insertion_sort

ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
}

ARRAY_SIZE = 20
ANIMATION_INTERVAL_MS = 150

DEFAULT_COLOR = "#4C78A8"
COMPARE_COLOR = "#F2A93B"
SWAP_COLOR = "#E45756"
SORTED_COLOR = "#54A24B"


def random_array(size=ARRAY_SIZE):
    return [random.randint(5, 100) for _ in range(size)]


def make_figure(array, comparing=None, swapped=None, sorted_idx=None):
    """Build a Plotly bar chart figure for one animation frame."""
    comparing = comparing or []
    swapped = swapped or []
    sorted_idx = sorted_idx or []

    colors = []
    for idx in range(len(array)):
        if idx in swapped:
            colors.append(SWAP_COLOR)
        elif idx in comparing:
            colors.append(COMPARE_COLOR)
        elif idx in sorted_idx:
            colors.append(SORTED_COLOR)
        else:
            colors.append(DEFAULT_COLOR)

    fig = go.Figure(
        data=[go.Bar(x=list(range(len(array))), y=array, marker_color=colors)]
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        yaxis=dict(range=[0, 110]),
        transition=dict(duration=0),  # we drive our own animation via Interval
    )
    return fig


app = Dash(__name__)
app.title = "Sorting Algorithm Visualizer"
server = app.server  # required by gunicorn for deployment

initial_array = random_array()

app.layout = html.Div(
    className="app-container",
    children=[
        html.H1("Sorting Algorithm Visualizer"),

        html.Div(
            className="controls",
            children=[
                dcc.Dropdown(
                    id="algo-dropdown",
                    options=[{"label": name, "value": name} for name in ALGORITHMS],
                    value="Bubble Sort",
                    clearable=False,
                    style={"width": "220px"},
                ),
                html.Button("Generate New Array", id="generate-btn", n_clicks=0),
                html.Button("Start", id="start-btn", n_clicks=0),
                html.Button("Reset", id="reset-btn", n_clicks=0),
            ],
        ),

        dcc.Graph(id="bar-chart", figure=make_figure(initial_array)),

        # Drives the animation: fires every ANIMATION_INTERVAL_MS while enabled
        dcc.Interval(id="interval", interval=ANIMATION_INTERVAL_MS, disabled=True),

        # --- Data stores (these replace needing a live Python generator object,
        # since Dash callbacks can't hold onto server-side objects between calls) ---
        dcc.Store(id="array-store", data=initial_array),   # the original unsorted array
        dcc.Store(id="frames-store", data=None),           # precomputed list of frames
        dcc.Store(id="index-store", data=0),                # which frame we're on
    ],
)


@app.callback(
    Output("array-store", "data"),
    Output("bar-chart", "figure", allow_duplicate=True),
    Output("frames-store", "data", allow_duplicate=True),
    Output("index-store", "data", allow_duplicate=True),
    Output("interval", "disabled", allow_duplicate=True),
    Input("generate-btn", "n_clicks"),
    prevent_initial_call=True,
)
def generate_new_array(n_clicks):
    arr = random_array()
    return arr, make_figure(arr), None, 0, True


@app.callback(
    Output("frames-store", "data", allow_duplicate=True),
    Output("index-store", "data", allow_duplicate=True),
    Output("interval", "disabled", allow_duplicate=True),
    Input("start-btn", "n_clicks"),
    State("algo-dropdown", "value"),
    State("array-store", "data"),
    prevent_initial_call=True,
)
def start_sort(n_clicks, algo_name, array):
    sort_fn = ALGORITHMS[algo_name]
    # Run the generator to completion up front, capturing every frame.
    # This sidesteps Dash's stateless callbacks (see note in app.py header).
    frames = list(sort_fn(array))
    return frames, 0, False  # enable the interval to start animating


@app.callback(
    Output("bar-chart", "figure", allow_duplicate=True),
    Output("frames-store", "data", allow_duplicate=True),
    Output("index-store", "data", allow_duplicate=True),
    Output("interval", "disabled", allow_duplicate=True),
    Input("reset-btn", "n_clicks"),
    State("array-store", "data"),
    prevent_initial_call=True,
)
def reset_view(n_clicks, array):
    return make_figure(array), None, 0, True


@app.callback(
    Output("bar-chart", "figure", allow_duplicate=True),
    Output("index-store", "data", allow_duplicate=True),
    Output("interval", "disabled", allow_duplicate=True),
    Input("interval", "n_intervals"),
    State("frames-store", "data"),
    State("index-store", "data"),
    prevent_initial_call=True,
)
def advance_frame(n_intervals, frames, current_index):
    if not frames or current_index >= len(frames):
        return no_update, no_update, True  # stop the interval, nothing left to show

    frame = frames[current_index]
    fig = make_figure(
        frame["array"],
        comparing=frame.get("comparing"),
        swapped=frame.get("swapped"),
        sorted_idx=frame.get("sorted_idx"),
    )
    next_index = current_index + 1
    is_last_frame = next_index >= len(frames)
    return fig, next_index, is_last_frame


if __name__ == "__main__":
    app.run(debug=True)