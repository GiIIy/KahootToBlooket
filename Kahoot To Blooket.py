import json
import requests
from openpyxl import load_workbook
import pandas as pd

# url must contain title!!!!!!!!!!!!!
url = input("Enter URL: ")
TLimit = input("Enter Time Limit: ")

kahoot_id = url.split('/')[-1]
answers_url = 'https://create.kahoot.it/rest/kahoots/{kahoot_id}/card/?includeKahoot=true'.format(kahoot_id=kahoot_id)
data = requests.get(answers_url).json()

title = url.split('/')[-2]
print("Title: {}".format(title))

questions = []
answers = []
Canswers = []

for q in data['kahoot']['questions']:
    questions.append('{:<70}'.format(q['question'].replace('&nbsp;', ' ')))
    for choice in q['choices']:
        
        if choice['correct']:
            Canswers.append("{}".format(choice['answer'].replace('&nbsp;', ' ')))
        
        answers.append("{} ".format(choice['answer'].replace('&nbsp;', ' ')))
    answers.append("NQ")

workbook = load_workbook(filename="blooket temp.xlsx")
sheet = workbook.active

row = 3
numQs = len(questions)

for x in range(numQs):
    sheet["B{}".format(row)] = questions[x]
    row +=1

iterat = 0
list1 = []

def colNumToLet(columna):
    if columna == 0:
        column = "C"
    elif columna == 1:
        column = "D"
    elif columna == 2:
        column = "E"
    elif columna == 3:
        column = "F"
    else:
        print("ERROR!!!")

    return column

row  = 3

while len(answers) > 0:
    for item in answers:
            if item == "NQ":

                break
            else:
                list1.append(item)
        
            column2  = colNumToLet(list1.index(item))
        
            sheet["{}{}".format(column2,row)] = item
    
    for z in list1:
        answers.remove(z)

    answers.remove("NQ")
    list1 = []
    row += 1
    
row = 3

for answer in Canswers:
    sheet["H{}".format(row)] = answer
    sheet["G{}".format(row)] = TLimit
    row += 1



workbook.save(filename="blooket temp.xlsx")

read_file = pd.read_excel (r'blooket temp.xlsx', sheet_name='Sheet1')
read_file.to_csv(r'BlooketImport.csv'.format(title), index = None, header=True)

