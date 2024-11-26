import pandas as pd
import numpy as np

data_frame = pd.read_csv("~/Downloads/open-context-24296-records(1).csv", low_memory=False)


data_count = data_frame.count()

print(data_count)

# human_bone = data_frame["Item Category"] #.count("Human Bone")

human_bone = data_frame['Item Category'].value_counts().get('Human Bone', 0)


print("item category, human bone:",human_bone)


uniques_item_cat = len(pd.unique(data_frame["Item Category"]))

print("unique item cat",uniques_item_cat)

unique_latitude = len(pd.unique(data_frame["Latitude (WGS 84)"]))
unique_longtittude = len(pd.unique(data_frame["Longitude (WGS 84)"]))

print("unique coords:", unique_longtittude,unique_latitude)

