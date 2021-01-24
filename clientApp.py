from flask import Flask, request, jsonify,render_template
import os
from flask_cors import CORS, cross_origin

import speechToText
import summ
from com_in_ineuron_ai_utils.utils import decodeSound

import moviepy.editor as mp

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRoute():
    print('in plot')
    if request.method=='POST':
        print('if')
        try:
            image = request.json['sound']
            # print('image',image)
            print('image')
            decodeSound(image, "video.mp4")
            print('decodeSound')
            clip = mp.VideoFileClip("video.mp4")
            print('clip video')
            clip.audio.write_audiofile("audio123.wav")
            print('clip audio')
            result = speechToText.speech2Text("audio123.wav")
            print('result')
            summary=summ.summarize(result)
            print('sssssssummary',summary)
            result='<h4 style=color:#273582>ORIGINAL TEXT:</h4>'+result+'<br>'+'<h4 style=color:#273582>SUMMARIZED TEXT:</h4>'+summary
            return jsonify({"Result" : str(result)})
            # return render_template('results.html')
            # return render_template('results.html',result=result,summary=summary)

        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'


#port = int(os.getenv("PORT"))
if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=port)
    app.run(host='0.0.0.0', port=5000, debug=True)