import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

from recipe_scrapers import scrape_me

import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
}


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch

def new_game():

    welcome_msg = render_template('welcome')
    reprompt_msg = render_template("welcome_reprompt")
    return question(welcome_msg).reprompt(reprompt_msg)


@ask.intent("AnswerIntent", mapping={'dish': 'dish'})

def answer(dish):

    dish = dish.replace(" ", "-")
    dish += "-"
    query = f"https://www.foodnetwork.com/search/{dish}"
    recipe = scrape_me()
    # $(".m-MediaBlock__a-Headline a")[0].href
    text = "Recipe for %s. Total time: %s. Here is the list of ingredients. %s" % (recipe.title(), recipe.total_time(), recipe.ingredients())
    return statement(text)

# self.soup.find('h1').get_text()
# self.soup.find('span', {'class': 'ready-in-time'})
# self.soup.findAll('li', {'class': "checkList__line"}

def search(url):
    drinks = requests.get(url).json()["drinks"]
    options = []
    for drink in drinks:
        dictionary = json.loads(parse_cocktail(drink))
        options.append(Cocktail(dictionary))
    return options

class Cocktail:
    def __init__(self, dictionary):
        self.name = dictionary["strDrink"]
        self.recipe = Cocktail.get_recipe(dictionary)
        self.instructions = dictionary["strInstructions"]

    @classmethod
    def get_recipe(cls, dictionary):
        ingredients = []
        measurements = []
        for key in dictionary:
            if "strIng" in key and dictionary[key]:
                ingredients.append(dictionary[key])
            if "strMea" in key and dictionary[key]:
                measurements.append(dictionary[key])

        if len(ingredients) != len(measurements):
            return []
        return ["%s %s" % (m, i) for m,i in zip(measurements, ingredients)]




if __name__ == '__main__':

    app.run(debug=True)
