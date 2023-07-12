from src.predict_bert import predict_main
import pandas as pd
from flask import Flask,request, jsonify, send_file,send_from_directory,render_template
import json

app = Flask(__name__,template_folder='templates') 
app.name ="bert"

# sentence_input = ["Minimum Alternate Tax (MAT) paid in accordance with the tax laws, which gives future economic benefits in the form of adjustment to future income tax liability, is considered as an asset if there is convincing evidence that the Company will pay normal income tax .",
# "Balances of Sundry Debtors, Creditors and Advances as at 31st March, 2019 are subject to confirmation .", 
# "Preliminary expenses have been written off in 5years. "]

@app.route('/bert_prediction', methods= ['GET', 'POST'])
def get_prediction() -> dict:
    json_data= json.loads(request.data, strict=False)

    sentence_input = json_data["Sentences"]
    print("sentence_input::",sentence_input)

    predicted_classes, probabilities, predicted_sub_class, probabilities_subclass = predict_main(sentence_input)
    # output_df = pd.DataFrame({"Statement" : sentence_input, "Class" : predicted_classes,"Class Probability" : probabilities, "Sub Class" : predicted_sub_class, "Sub Class Probability" : probabilities_subclass})
    # output_df.to_excel("BERT_output.xlsx", index=False)

    json_output = {"Statement" : sentence_input, "Class" : predicted_classes,"Class Probability" : probabilities, "Sub Class" : predicted_sub_class, "Sub Class Probability" : probabilities_subclass}
    return json.dumps(json_output)



if __name__ == "__main__":

    """

    python app.py
    
    """
    # Logger_init()
    app.run(host="0.0.0.0", port="8010", debug=False)