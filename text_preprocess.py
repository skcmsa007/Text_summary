import re





text="This adjustment is due to excess/(short) depreciation charged till March 31, 2018 and the same has been directly appropriated to reserve & surplus without routing it to the P & L account *Note: This adjustment is due to excess/(short) depreciation charged till March 31, 2018 and the same has been directly appropriated to reserve & surplus without routing it to the P & L account 76"
print(text)
print("------------------------------")
y=re.sub("[\(\[].*?[\)\]]", "", text)
print(y)