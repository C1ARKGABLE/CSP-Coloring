import json
import time
import random
from pprint import pprint
import plotly.express as px
import plotly.graph_objects as go

valid_colors = ["R", "G", "B", "Y"]


def promising(color, neighbors, states_dict):
    for neighbor in neighbors:
        if color == states_dict[neighbor]["color"]:
            return False

    return True


# def color_for_state(state, states_dict):
#     for color in states_dict[state]["valid"]:
#         if promising(color, states_dict[state]["constraints"], states_dict):
#             return color


# def csp_dfs(states, states_dict):
#     for state in states:
#         states_dict[state]["color"] = color_for_state(state, states_dict)

#     return states_dict


def csp_dfs(
    states, states_dict, index=0, fwd=False, single=False,
):
    states_dict_copy = states_dict.copy()

    # if "" not in [states_dict[state]["color"] for state in states]:
    #     return states_dict
    if index >= len(states):
        return states_dict
    else:
        state = states[index]
        for color in states_dict[state]["valid"]:
            if promising(color, states_dict[state]["constraints"], states_dict):
                states_dict[state]["color"] = color
                states_dict = csp_dfs(
                    states, states_dict, index=index + 1, fwd=fwd, single=single,
                )

            # if fwd:
            #     for neighbor in states_dict[state]["constraints"]:
            #         valid_colors[neighbor] ^= set([color])
            #         if len(valid_colors[neighbor]) <= 0:
            #             print(f"Fail {neighbor}")
            #             return states_dict_copy, valid_colors_copy
            #         elif single and len(valid_colors[neighbor]) == 1:
            #             single_valid_color = valid_colors[neighbor].pop()
            #             states_dict[neighbor]["color"] = single_valid_color
            #             valid_colors[neighbor] = set([single_valid_color])
            #             index += 1

        return states_dict_copy


def order_states(states_dict, hueristic=None):
    states = list(states_dict.keys())

    if hueristic == "MRV":
        return states
    elif hueristic == "Degree Constraint":
        return states
    elif hueristic == "Least Constraining Value":
        return states
    else:
        random.shuffle(states)

    return states


if __name__ == "__main__":
    with open("AU.json", "r") as f:
        master = json.load(f)
        states_dict = master["constraints"]
        geojson = master["geo"]

    states = order_states(states_dict)

    for state in states:
        states_dict[state]["valid"] = valid_colors

    final_dict = csp_dfs(states, states_dict)

    fig = go.Figure(
        px.choropleth(
            locations=list(final_dict.keys()),
            geojson=geojson,
            featureidkey="properties.id",
            color=[final_dict[state]["color"] for state in list(final_dict.keys())],
            color_discrete_sequence=px.colors.qualitative.Antique,
            projection="mercator",
        )
    )
    fig.update_geos()
    fig.update_geos(
        fitbounds="locations",
        visible=False,
        resolution=110,
        showcountries=True,
        countrycolor="Black",
    )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()


# def valid_color_choice(color, state, states_dict):
#     for neighbor in states_dict[state]["constraints"]:
#         if color == states_dict[neighbor]["color"]:
#             return False
#     return True