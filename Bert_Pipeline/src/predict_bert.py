import json
import os
import requests
from bert import tokenization
import numpy as np
import pandas as pd
import grpc
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc
import tensorflow as tf
import configparser

config = configparser.ConfigParser()
config.read("./src/config.ini")

# example = "Balances of Sundry Debtors, Creditors and Advances as at 31st March, 2019 are subject to confirmation ."
# example = "In the absence of information from creditors of their status, the amount due to trade payables is not ascertainable ."
# example = "Preliminary expenses have been written off in 5years. "

# sentence_input = [" measurement and/or disclosure purposes in these financial Sun Pharmaceutical Industries Limited (the Company') is a Statements is determined on such a basis, except for share- publiclimited company incorporated and domiciled in India, based payment transactions that are within the scope of Ind AS having it's registered office at Vadodara, Gujarat, India and 102, leasing transactions that are within the scope of Ind AS has its listing on the Bombay Stock Exchange Limited and 17, and measurements that have some similarities to fair value National Stock Exchange of India Limited. The Company is in but are not fair value, such as net realisable value in Ind AS 2 or the business of manufacturing, developing and marketing a value in use in Ind AS 36. Wide range of branded and generic formulations and Active In addition, for financial reporting purposes, fair value Pharmaceutical Ingredients (APIs). The Company has various manufacturing locations spread across the country with trading measurements are categorised into Level 1, 2, or 3 based on the degree to which the inputs to the fair value measurements and other incidental and related activities extending to the global markets. are observable and the significance of the inputs to the fair value measurement in its entirety, which are described as The standalone financial statements were authorised for issue in follows: accordance with a resolution of the directors on May 25, 2018. Level 1 inputs are quoted prices (unadjusted) in active markets for identical assets or liabilities that the entity can access at the measurement date; These financial statements are separate financial statements Level 2 inputs are inputs, other than quoted prices included of the Company (also called standalone financial statements). within Level 1, that are observable for the asset or liability, The Company has prepared financial statements for the year either directly or indirectly; and ended March 31, 2018 in accordance with Indian Accounting Level 3 inputs are unobservable inputs for the asset or Standards (Ind AS) notified under the Companies (Indian liability. Accounting Standards) Rules, 2015 (as amended) together with the comparative period data as at and for the year ended The Company has consistently applied the following March 31, 2017. accounting policies to all periods presented in these financial Statements. The financial statements have been prepared on the historical cost basis, except for: (i) certain financial instruments that are The Company presents assets and liabilities in measured at fair values at the end of each reporting period; (ii) Non-current assets classified as held for sale which are the balance sheet based on current / non-current measured at the lower of their carrying amount and fair value classification. An asset is treated as current when it is: less costs to sell; (iii) derivative financial instrument and (iv) Expected to be realised or intended to be sold or defined benefit plans- plan assets that are measured at fair Consumed in normal operating cycle values at the end of each reporting period, as explained in the accounting policies below: Held primarily for the purpose of trading Historical cost is generally based on the fair value of the Expected to be realised within twelve months after the consideration given in exchange for goods and services. reporting period, or The standalone financial statements are presented in ₹ and all Cash or cash equivalent unless restricted from being values are rounded to the nearest Million (₹ 000,000) upto one exchanged or used to settle a liability for at least twelve decimal, except when otherwise indicated. months after the reporting period All other assets are classified as non-current. Fair value is the price that would be received to sell an asset or paid to transfer a liability in an orderly transaction between A liability is current when: market participants at the measurement date, regardless of t is expected to be settled in normal operating cycle whether that price is directly observable or estimated using another valuation technique. In estimating the fair value of It is held primarily for the purpose of trading an asset or a liability, the Company takes into account the characteristics of the asset or liability if market participants t is due to be settled within twelve months after the would take those characteristics into account when pricing the asset or liability at the measurement date. Fair value for reporting period, or"]
# print("length of sentence :::", len(sentence_input[0]))

def data_preprocessing(example):
    tokenizer = tokenization.FullTokenizer(vocab_file=config['BERT']['vocab_file'], do_lower_case=True)
    token_a = tokenizer.tokenize(example)

    tokens = []
    segments_ids = []
    tokens.append("[CLS]")
    segment_ids = []
    segment_ids.append(0)
    for token in token_a:
        tokens.append(token)
        segment_ids.append(0)

    tokens.append('[SEP]')
    segment_ids.append(0)

    input_ids = tokenizer.convert_tokens_to_ids(tokens)
    input_mask = [1] * len(input_ids)
    max_seq_length = 128
    # print("length of input_ids :::", len(input_ids))
    while len(input_ids) < max_seq_length:
        input_ids.append(0)
        input_mask.append(0)
        segment_ids.append(0)

    label_id = 0

    return input_ids, input_mask, segment_ids

def preprocess_data(data):
    input_ids, input_mask, segment_ids, label_id = [], [], [], []
    for each_item in data:
        processed_output = data_preprocessing(each_item)
        input_ids.append(processed_output[0])
        input_mask.append(processed_output[1])
        segment_ids.append(processed_output[2])
        label_id.append(0)
    return input_ids, input_mask, segment_ids, label_id

def get_prediction(data, grpc_channel, req_timeout):
   
    input_ids, input_mask, segment_ids, label_id = data
    options = [('grpc.max_message_length', 16 * 10000 * 10000),
                            ('grpc.max_receive_message_length', 16 * 10000 * 10000)]
    channel = grpc.insecure_channel(grpc_channel, options = options)
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
    grpc_request = predict_pb2.PredictRequest()
    grpc_request.model_spec.name = 'bert'
    grpc_request.model_spec.signature_name = 'serving_default'
    input_ids = np.array(input_ids).astype("int32")
    input_mask = np.array(input_mask).astype("int32")
    segment_ids = np.array(segment_ids).astype("int32")
    label_id = np.array(label_id).astype("int32")
    grpc_request.inputs['input_ids'].CopyFrom(tf.make_tensor_proto(input_ids,shape=input_ids.shape))
    grpc_request.inputs['input_mask'].CopyFrom(tf.make_tensor_proto(input_mask,shape=input_mask.shape))
    grpc_request.inputs['segment_ids'].CopyFrom(tf.make_tensor_proto(segment_ids,shape=segment_ids.shape))
    grpc_request.inputs['label_ids'].CopyFrom(tf.make_tensor_proto(label_id,shape=label_id.shape))


    result = stub.Predict(grpc_request, int(req_timeout))
    output = result.outputs
    raw_output = tf.make_ndarray(output["probabilities"])
    return raw_output


def predict_child(preprocessed_data, class_type, grpc_channel, req_timeout, index):
    bs_classes = ["EQ", "NCL", "CL", "NCA", "CA"]
    is_classes = ['REV', 'OI', 'COGS', 'DEP', 'FC', 'OE', 'NOE', 'NOI', 'TAX', 'KM1', 'KM2', 'KM3', 'EEPP', 'KM4', 'KM5']
    cf_classes = ["CFO", "CFI", "CFF"]

    classes_dict = {"BS":bs_classes, "IS":is_classes ,"CF":cf_classes}

    input_ids, input_mask, segment_ids, label_id = preprocessed_data
    preprocessed_data = input_ids[index:index+1], input_mask[index:index+1], segment_ids[index:index+1], label_id[index:index+1]
    raw_output = get_prediction(preprocessed_data, grpc_channel, req_timeout )
    # print("raw_output:", raw_output)    
    raw_output = raw_output[0]
    classes = classes_dict[class_type]

    predicted_class = classes[np.argmax(raw_output)]
    probability = raw_output[np.argmax(raw_output)] * 100

    # print("Sub Class::", predicted_class)
    # print("Sub Class probability::", probability)

    return predicted_class,probability





def predict_main(data):
    req_timeout = config['BERT']['req_timeout']
    grpc_channel_main = config['BERT']['grpc_channel_main']
    grpc_channel_bs = config['BERT']['grpc_channel_bs']
    grpc_channel_is = config['BERT']['grpc_channel_is']
    grpc_channel_cf = config['BERT']['grpc_channel_cf']

    # print("grpc_channel_main:::", grpc_channel_main)

    grpc_channel_dict = {"BS": grpc_channel_bs, "IS": grpc_channel_is ,"CF" : grpc_channel_cf}

    preprocessed_data = preprocess_data(data)
    raw_output = get_prediction(preprocessed_data, grpc_channel_main, req_timeout)
    predicted_classes, probabilities = [], []
    predicted_sub_class, probabilities_subclass = [], []
    sub_class = None
    sub_class_prob = np.nan
    classes = ["BS", "IS", "CF", "Others", "Risk"]
    for index, each_output in enumerate(raw_output):
        predicted_class = classes[np.argmax(each_output)]
        probability = each_output[np.argmax(each_output)]*100
        # print("predicted_class::",predicted_class)
        if(predicted_class in ["BS", "IS", "CF"]):
            sub_class, sub_class_prob = predict_child(preprocessed_data, predicted_class, grpc_channel_dict[predicted_class], req_timeout, index)

        predicted_classes.append(predicted_class)
        probabilities.append(probability)
        predicted_sub_class.append(sub_class)
        probabilities_subclass.append(sub_class_prob)

    

    return predicted_classes, probabilities, predicted_sub_class, probabilities_subclass


