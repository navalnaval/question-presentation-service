import json
import requests
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/quetionandresults', methods=['GET'])
def provideQuestionAndResults():
        try:
                queReq = requests.get(url='https://api.mentimeter.com/questions/48d75c359ce4', headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'})
                queContent = queReq.json()
                if 'status' in queContent and queContent['status'] == 403:
                        raise Exception('Could not reach question API!')
                if not 'question' in queContent:
                        raise Exception('Question content is missing!')
                resReq = requests.get(url='https://api.mentimeter.com/questions/48d75c359ce4/result', headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'})
                resContent = resReq.json()
                if 'status' in resContent and resContent['status'] == 403:
                        raise Exception('Could not reach results API')
                if not 'results' in resContent:
                        raise Exception('Results content is missing!')

                contentToRespond = json.dumps({'question': queContent['question'], 'results': resContent['results']})
                response = app.response_class(
                        response=contentToRespond,
                        status=200,
                        mimetype='application/json'
                )
        except:
                response = app.response_class(
                        response='Something went wrong!',
                        status=500
                )

        return response

if __name__ == "__main__":
        print("hello mentimeter!")
        app.run(host='0.0.0.0', port=9002, debug=True)