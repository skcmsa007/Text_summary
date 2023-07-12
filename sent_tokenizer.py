import requests
import ast
import json

stanza_url="http://13.126.27.92:8069"
text  = " Write down of inventories  to net realizable value amounted to ₹ 612 crore . These were recognized as expense and included in 'Cost of Material Consumed' and 'Changes in Inventories of Finished Goods, Work-in-Progress and Stock-in-Trade' in the Consolidated Statement of Profit and Loss. Inventories in hand include bulk material of coa, bauxite and copper concentrate lying at yards, mines, plants, precious metals of gold and silver ying at smelter and refinery aggregating to ₹ 4,302 crore ."
stanza_dict = {"sentence": text}

doc_op = requests.post(stanza_url, json=stanza_dict).text
doc = ast.literal_eval(doc_op)
number_of_sent=len(doc["sent_list"])
print(doc["sent_list"])
#tokens = [sent for sent in doc["sent_list"]]

# print(len(tokens))