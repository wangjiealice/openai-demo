import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        question = request.form["question"]
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
               {"role": "system", "content": "You are a helpful assistant."},
               {"role": "user", "content": question},
            ]
			)
        
        return redirect(url_for("index", result=response.choices[0].message.content))

    result = request.args.get("result")
    return render_template("index.html", result=result)

@app.route('/correct',methods=['GET','POST'])
def correct():
#    if request.method == "GET":
#        result = "1111111"
#        result1 = "2222222"
#        return render_template("index.html", result1=result1,result=result)
    if request.method == "POST":
        textToCorrect = request.form["textToCorrect"]
        response = openai.Completion.create(
          model="text-davinci-003",
          prompt="Correct this to standard English:\n\nShe no went to the market.",
          temperature=0,
          max_tokens=60,
          top_p=1.0,
          frequency_penalty=0.0,
          presence_penalty=0.0
        )
        return redirect(url_for("correct", result=response.choices[0].text))

    result1 = request.args.get("result")
    return render_template("index.html", result1=result1)

@app.route('/image',methods=['GET','POST'])
def imageFunction():
    if request.method == "POST":
        imageContent = request.form["imageContent"]
#        imageUrl = "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fsafe-img.xhscdn.com%2Fbw1%2Fd5e02748-f605-4be6-900b-cee6f93bbcdd%3FimageView2%2F2%2Fw%2F1080%2Fformat%2Fjpg&refer=http%3A%2F%2Fsafe-img.xhscdn.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1683512584&t=0bf2768997638065bebc5edf5baed5ae"
        response = openai.Image.create(
#          prompt="a white siamese cat",
          prompt=imageContent,
          n=2,
          size="256x256"
        )
        image_url1 = response['data'][0]['url']
        image_url2 = response['data'][1]['url']
        return redirect(url_for("imageFunction", result1=image_url1,result2=image_url2))

    imageUrl1 = request.args.get("result1")
    imageUrl2 = request.args.get("result2")
    return render_template("index.html",
                           displayImageSrc1 = imageUrl1,displayImageSrc2 = imageUrl2)

@app.route("/audio", methods=("GET", "POST"))
def audio():
    if request.method == "POST":
        audio_file = open(os.getcwd() + "/static/friend.mp3", "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return redirect(url_for("audio", returnValue=transcript.text))

    audioResult = request.args.get("returnValue")
    return render_template("index.html", audioResult=audioResult)

@app.route("/audioTranslation", methods=("GET", "POST"))
def audioTranslation():
    if request.method == "POST":
        audio_file = open(os.getcwd() + "/static/roof.mp3", "rb")
        transcript = openai.Audio.translate("whisper-1", audio_file)
        return redirect(url_for("audioTranslation", returnValue=transcript.text))

    audioTranslationResult = request.args.get("returnValue")
    return render_template("index.html", audioTranslationResult=audioTranslationResult)