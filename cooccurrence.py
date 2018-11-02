from os import listdir
from os import system
from imgdl import read_csv
import itertools

#Gets the id from the filename which has the format: id.txt
def getID(filename):
    return filename.split('.')[0]

#Directory containing the results.
fileDirectory = "./results/"   
fileList = listdir(fileDirectory)

#formate -  object : id
object_list = {}

# get the image ids with their corresponding privacy settings
# id_privacy dictionary has the format - image_id : privacy_setting
ids, id_privacy = read_csv("cleaned.csv");

"""
Format of hte result file:
./train/xxx.jpg: Predicted in xxx.xxx seconds.
object1: xx%
object2: xx%
...
"""
#read each result file and extract objects, then link each object to its privacy setting
i = 0
for filename in fileList:
    with open("results/" + filename) as r_f:
        for line in r_f:
            if line[0] != '.':
                if (line.split(':')[0]) not in object_list:
                    i += 1
                    object_list[line.split(':')[0]] = i


cooccurrency_matrix = [[ x * 0 for x in range(i)] for y in range(i)]
privacy_matrix = [[ x * 0 for x in range(i)] for y in range(i)]

for filename in fileList:
    with open("results/" + filename) as r_f:
        objects = []
        for line in r_f:
            if line[0] != '.':
                # line.split(':')[0] is the object string
                objects.append(object_list[line.split(':')[0]])
        if len(objects) > 1:
            for i, j in itertools.combinations(objects, 2):
                cooccurrency_matrix[i][j] += 1
                cooccurrency_matrix[j][i] += 1
                if id_privacy[getID(filename)] == "private":
                    privacy_matrix[i][j] -= 1
                    privacy_matrix[j][i] -= 1
                elif id_privacy[getID(filename)] == "public":
                    privacy_matrix[i][j] += 1
                    privacy_matrix[j][i] += 1