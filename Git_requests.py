import os
import json
import requests
import pandas as pd

from text_preprocessing import text_cleaning

current_directory = os.getcwd()

'''------------ For downloading the issues ------------------'''

def fetch_issue_byID(issue_ID):
    try:
        owner = "spring-projects"
        repo = "spring-boot"
        path = f"/repos/{owner}/{repo}/issues/{issue_ID}"
        url = f"https://api.github.com{path}"
        blank = {}
        response = requests.get(url)
        output = json.loads(response.text)
        print(issue_ID)
        with open(f'{current_directory}/issue_database/{issue_ID}.json', 'w') as fp:
            json.dump(output, fp)        
    except Exception as e:
        print(e)

# for i in range(30884 , 31000):
#     fetch_issue_onebyone(i)


'''-------------- for cleaning data-----------------'''

def clean_file(file_name):
    try:
        blank_1 = {}

        f = open(f"{current_directory}/issue_database/{file_name}")
        issue = json.load(f)
        blank_1["title"] = issue["title"]
        blank_1['body'] = issue["body"]
        blank_1['state'] = issue["state"]
        if issue.__contains__("labels"):
            blank_1['tag'] = issue["labels"][0]["name"]
        blank_1['url'] = issue["url"]
        issue_id = issue["url"].split("/")[-1]
            
        with open(f'{current_directory}/clean_issue_database/{file_name}', 'w') as fp:
            json.dump(blank_1, fp)

        if "clean_dataframe.csv" not in os.listdir(f"{os.getcwd()}/clean_issue_database"):
            # print(os.listdir(f"{os.getcwd()}/clean_issue_database"))
            # Creating a fresh dataframe if not exist
            clean_dataframe = pd.DataFrame(columns=['issue_ID','title', 'body', 'state', 'tag'])
            clean_dataframe.loc[0,"issue_ID"] = issue_id
            clean_dataframe.loc[0,"title"] = text_cleaning(issue["title"])
            if issue["body"] != None:
                clean_dataframe.loc[0,"body"] = text_cleaning(issue["body"])
            else:    
                clean_dataframe.loc[0,"body"] = issue["body"]
            clean_dataframe.loc[0,"state"] = issue["state"]
            if issue.__contains__("labels"):
                clean_dataframe.loc[0,"tag"] = issue["labels"][0]["name"]
            clean_dataframe.to_csv(f"{current_directory}/clean_issue_database/clean_dataframe.csv")
        else:
            clean_dataframe = pd.read_csv(f"{os.getcwd()}/clean_issue_database/clean_dataframe.csv",index_col=[0])
            index_number = clean_dataframe.shape[0]
            # print(index_number)
            clean_dataframe.loc[index_number,"issue_ID"] = issue_id
            clean_dataframe.loc[index_number,"title"] = text_cleaning(issue["title"])
            if issue["body"] != None:
                clean_dataframe.loc[index_number,"body"] = text_cleaning(issue["body"])
            else:    
                clean_dataframe.loc[index_number,"body"] = issue["body"]
            clean_dataframe.loc[index_number,"state"] = issue["state"]
            if issue.__contains__("labels"):
                clean_dataframe.loc[index_number,"tag"] = issue["labels"][0]["name"]
            clean_dataframe.to_csv(f"{current_directory}/clean_issue_database/clean_dataframe.csv")
    except Exception as e:
        print(e)

# for i in os.listdir(f"{path}/dataset"):
#     clean_file(i)
