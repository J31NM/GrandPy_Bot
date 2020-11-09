from flask import Flask, render_template, request, jsonify
import requests
from gpb_app.api_manager import Parser
from gpb_app.api_manager import WikiAPI

app = Flask(__name__)
# To get one variable, tape app.config['MY_VARIABLE']
app.config.from_object('config')
parser = Parser()
wiki = WikiAPI()



@app.route("/", methods=["GET"])
def retrieve():
    return render_template('index.html')


@app.route("/sendRequest/")
def results():
    parsed_result = parser.parse(request.args.get("query"))
    output = wiki.get_wiki_output(parsed_result)
    return jsonify(output)


if __name__ == '__main__':
    app.run(debug=True)
