from flask import Flask, render_template, request, jsonify
import random
from gpb_app.api_manager import Parser
from gpb_app.api_manager import WikiAPI
from gpb_app.api_manager import MapsAPI

app = Flask(__name__)
# To get one variable, tape app.config['MY_VARIABLE']
app.config.from_object('gpb_app.constants')
parser = Parser()
wiki = WikiAPI()
maps = MapsAPI()

# List of random sentences for Grandpy if the request fails
fail = ["Je n'ai pas compris ta question....",
        "Parle plus fort, papy est sourd....",
        "Jamais entendu parler. Parlons d'autre chose....",
        "..."
    ]

# List of random sentences for Grandpy if the request succed
answer = ["Ah oui ça me parle, savais tu que :",
          "Mon lieu favori. Je sais plein de choses à son sujet, par exemple :",
          "J'y suis allé une fois. J'ai retenu que :"
    ]


@app.route("/", methods=["GET"])
def retrieve():
    """
    Load index.html front home page

    :return:
    """
    return render_template('index.html')


@app.route("/sendRequest/")
def results():
    """
    Data to send after user click request

    :return: data for front :
        _ coordinates to display Google Map
        _ text from WikiMedia for GrandPy knowledge
        _ answer from GrandPy, good or bad depend on request success
    """
    # parse the user input to get a words list
    parsed_result = parser.parse(request.args.get("query"))
    try:
        # Use Wikipedia object to get the grandpy knowledge for the user from wikiMedia
        gp_wiki = wiki.wikier(parsed_result)
        # Use Maps object to get the place coordinates from Google Maps
        coordinates = maps.get_maps_output(parsed_result)
        # return data for the front
        return jsonify(coordinates=coordinates,
                       text=gp_wiki,
                       answer=random.choice(answer))

    except:
        # return error message for the front if the request fails
        return jsonify(error_message=random.choice(fail))


if __name__ == '__main__':
    app.run(debug=True)

