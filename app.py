import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        idea = request.form["idea"]
        response = openai.Completion.create(
            max_tokens=500,
            model="text-davinci-003",
            prompt=generate_prompt(idea),
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    image_list = []
    result_list = []
    if (result):
        result_list = result.split(".")

        for r in result_list:
            print(r)
            response = openai.Image.create(
                prompt=r + ",  in the syle of flat art and without text",
                n=1,
                size="256x256"
            )
            image_url = response['data'][0]['url']
            print(image_url)
            image_list.append(image_url)

    return render_template("index.html", result=result, result_list=result_list, image_list=image_list)


def generate_prompt(idea):
    return """Create a user storymap based on six sentences for a product

Product: A self watering pot
Storymap: The user wants to water their plants, but keeps forgetting about it. The user buys the self watering pot. The user configures the self watering pot by selecting the type of plant. The pot configures the amount of water based on the type of plant. The self watering pot waters the plants. The self watering pot warns the user when the water level is low.
Product: An app targeted to kids who go on school trips to fish, that will use the app to register marine species and keep track of the number of specimen.
Storymap: It is hard to keep track of the number of marine specimen. By using the app, the user is able to register the marine species they encounter. When the user encounters an especiment, they can add a picture, the species, time and location. The app saves all the information and displays to the users the number of specimen in a map. The apps offers the possibility of sharing the specimen with others.
Product: {}
Storymap:""".format(
        idea.capitalize()
    )
