from flask import Flask, render_template, jsonify, request
import threading
import webbrowser
import time
import subprocess
import sys
import argparse
import json
import glob
"""
    TryThisAtHome Server
"""

# Construct Server
app = Flask(__name__)

###### Load user data
user_filename = "./user.json"
with open(user_filename, "r") as f:
    user_data = json.load(f)


###### Load experiments
files = glob.glob('./experiments/*.json')
experiments = []
for file in files:
    with open(file, "r") as f:
        experiments.append(json.load(f))


# User data accessed by server requests
app.data = {
    "user_filename": user_filename,
    "user": user_data,
    "experiments": experiments
}

# Diff two liusts, thanks: https://www.geeksforgeeks.org/python-difference-two-lists/
def diff(li1, li2): 
    return (list(set(li1) - set(li2)))

@app.route('/')
def index():
    return browse()

@app.route('/inventory')
def inventory():
    # Unique experiment items
    inventory = app.data["user"]["inventory"]
    ingredients = []
    for experiment in app.data["experiments"]:
        ingredients.extend(experiment["ingredients"])

    return render_template('inventory.html', **{
        "inventory": inventory,
        "ifonly": diff(ingredients, inventory)
    })

@app.route('/inventoryUpdate', methods=['POST'])
def inventory_update():
    # Update user
    inventory = request.form.getlist('inventory[]')
    app.data["user"]["inventory"] = inventory

    # # Serialise
    # with open(app.data["user_filename"], "w") as f:
    #     json.dump(app.data["user"],f,indent=4)

    return "done"

@app.route('/reccomendations')
def reccomendations(max_reqs=3):
    # Initialise
    experiments_by_reqs = {}

    for experiment in app.data["experiments"]:
        diffed = diff(experiment["ingredients"], app.data["user"]["inventory"])
        reqs = len(diffed)
        if reqs <= max_reqs:
            title = ""
            if reqs == 0:
                title = "Ready to go"
            else:
                title = "%i items needed" % reqs

            if title not in experiments_by_reqs:
                experiments_by_reqs[title] = []

            experiments_by_reqs[title].append(experiment)

    print(experiments_by_reqs)

    return render_template('reccomendations.html', **{
        "experiments": experiments_by_reqs
    })

@app.route('/browse')
def browse():
    ingredients = []
    edge_data = []
    for experiment in experiments:
        # Take stock
        ingredients.extend(experiment["ingredients"])

        # Mark edges
        for ingredient in experiment["ingredients"]:
            edge_data.append({
                "from": ingredient,
                "to": experiment["name"]
            })

    # Uniqueify ingredients
    ingredients = list(set(ingredients))

    # Generate Node data
    ingredient_nodes = [{
        "id": ingedient,
        "label": ingedient,
        "color": "red"
    } for ingedient in ingredients]

    experiment_nodes = [{
        "id": experiment["name"],
        "label": experiment["name"],
        "color": "white"
    } for experiment in experiments]

    return render_template('browse.html', **{
        "nodes": ingredient_nodes + experiment_nodes,
        "edges": edge_data
    })



def main(args):
    """
        Run server
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--open", action="store_true")
    parser.add_argument("--host", default="127.0.0.1", help="host")
    parser.add_argument("--port", default=5000, help="port")

    parsed = parser.parse_args(args)

    app.run(debug=True, host=parsed.host, port=parsed.port)

if __name__ == '__main__':
    main(sys.argv[1:])
