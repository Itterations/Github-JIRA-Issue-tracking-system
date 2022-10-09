import json
import os
import pandas as pd
import string
from flask import Flask , jsonify, request
import numpy as np

app = Flask(__name__)
current_directory = os.getcwd()
encoding_path = f"{os.getcwd()}/embeddings"

# Importing codes related to Github issue fetching
from Git_requests import fetch_issue_byID , clean_file

# Importing functions for text preprocessing
from text_preprocessing import text_cleaning


'''---------Loading Transformer model------------'''
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


from scipy import spatial
def cosine_similiarity(text):
    embd_vect = model.encode(text_cleaning(text))
    clean_dataframe = pd.read_csv(f"{current_directory}/clean_issue_database/clean_dataframe.csv")
    computation = clean_dataframe.copy()
    for i in range(computation.shape[0]):
        embeding_path = computation.loc[i,"embeddings"]
        with open(embeding_path, 'rb') as f:
            a = np.load(f)
        cosine_sim= 1 - spatial.distance.cosine(a, embd_vect)
        computation.loc[i,"Cosine_Similiarity"] = cosine_sim
    output = computation.sort_values('Cosine_Similiarity',ascending=False).head(5)
    output.to_csv(f"{current_directory}/Top5Similiar.csv")

'''---------Loading Transformer model------------'''



'''------------------ internal Codes-----------------------'''
print("API loading ..................")
for file_name in os.listdir(f"{current_directory}/issue_database"):
    if file_name not in os.listdir(f"{current_directory}/clean_issue_database"):
        clean_file(file_name=file_name)

clean_dataframe = pd.read_csv(f"{current_directory}/clean_issue_database/clean_dataframe.csv")
column_list  = clean_dataframe.columns.values.tolist()
if "embeddings" not in column_list:
    for i in range(clean_dataframe.shape[0]):
        title = clean_dataframe.loc[i,"title"]
        issue_ID = int(clean_dataframe.loc[i,"issue_ID"])
        encod_vect = model.encode(title)
        filename = f"{encoding_path}/{issue_ID}.npy"
        with open(filename, 'wb') as f:
            np.save(f, encod_vect)
        clean_dataframe.loc[i,"embeddings"] = filename
    clean_dataframe.to_csv(f"{current_directory}/clean_issue_database/clean_dataframe.csv")

'''------------------ internal Codes-----------------------'''

'''*****************************************************************************************'''



'''---------------- API functions below------------------'''
@app.route('/')
def homepage():
    return jsonify({"message" : "Hi,The API is ready to use now................."})            


@app.route('/NewIssue',methods= ["GET"])
def NewIssue():
    # try:
    data = request.get_json()
    title = data["title"]
    print(f"--------------->>>>>>>>>>{title}")
    body = data["body"]
    cosine_similiarity(title)
    return jsonify({"Successful":"Top 5 issue have been tracked,please check the file --> Top5Similiar.csv"})
    # except Exception as e:
    #     print(e)
    #     return jsonify({"Error": " There is some bug in the code, Please check"})

'''---------------- API functions above-------------------'''


if __name__=="__main__":
    app.run(host = 'localhost',port='8899',debug=True)

