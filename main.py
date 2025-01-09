from flask import Flask, render_template, request
import markdown
import module, json


GoogleKey = "AIzaSyDcSBAvY8z8TkvG2HTe1ky_VOtxzy9Q0x0"
DatabaseEndpoint = "https://08104d52-e171-44d1-8440-89586a84498a-us-east-2.apps.astra.datastax.com"


app = Flask("AstraDB Integrated Project")
import google.generativeai as genai
genai.configure(api_key=GoogleKey)
model = genai.GenerativeModel("gemini-1.5-pro-latest")


@app.route('/')
def home():
    return render_template("landing.html")

@app.route('/analyse')
def analyse():
    return render_template("analisis.html")

@app.route('/html', methods=["POST"])
def html():
    data = request.get_json()
    mark = data.get('markdown', '')
    processed_data = markdown.markdown(mark)
    return processed_data, 200

@app.route('/process', methods=["POST","GET"])
def process():
    data = request.get_json()
    query = data.get('query', '')
    if query == '':
        return "",200
    else:
        processed_data = module.main(query)
    return processed_data, 200

@app.route('/jsonif', methods=["POST","GET"])
def improve():
    data = request.get_json()
    prompt = data.get('prompt', '')
    if prompt == '':
        response = json.dumps({
            "count":0,
            "Max_likes": 0,
            "Max_comments": 0,
            "Max_shares": 0,
            "Avg_likes": 0,
            "Avg_comments": 0,
            "Avg_shares": 0,
            "Correlation": {
                "Likes2Comments": 0,
                "Likes2Shares": 0,
                "Share2Comments": 0
            },
            "Ratio": {
                "Likes2Comments": 0,
                "Likes2Shares": 0,
                "Share2Comments": 0
            },
            "Highest": {
                "post_type": "--",
                "likes": 0,
                "comments": 0,
                "shares": 0
            }
        })
    else:
        response = model.generate_content("""analyse the given text and extract the information based on the supplied schema in JSON Format, if text doesn't contain the exact data that needs to be extracted then it must set "--" or 0 in its place in JSON schema,
        Given text is:
        ---                                
        """+prompt+"""
        --- 
        Use this JSON schema:
        Report = {
            "count":int,
            "Max_likes":int,
            "Max_comments":int,
            "Max_shares":int,
            "Avg_likes":int,
            "Avg_comments":int,
            "Avg_shares":int,
            "Correlation":{
                "Likes2Comments":float,
                "Likes2Shares":float,
                "Share2Comments":float
            },
            "Ratio":{
                "Likes2Comments":float,
                "Likes2Shares":float,
                "Share2Comments":float
            },
            "Highest":{
                "post_type":str,
                "likes":int,
                "comments":int,
                "shares":int
            }
        }
        Return Report
        """)
        print("Response Formated")
        txt = response.text
        response = txt[txt.find('```json')+7:txt.find('```',txt.find('```json')+7)]
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000, debug=True)
