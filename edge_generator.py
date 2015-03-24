
import string
from model.edge import Edge
alphabet_list = list(string.ascii_uppercase)



def readValueFromFile(filePath):

    input_file = open(filePath)
    number_of_cities = input_file.readline()
    costs = input_file.readline().rstrip('\n').split(',')
    reliabilities = input_file.readline().rstrip('\n').split(',')
    return number_of_cities,costs,reliabilities


def generate(filePath):
    number_of_cities, costs,reliabilities = readValueFromFile(filePath)
    city_list = alphabet_list[0:int(number_of_cities)]
    edge_list = list()
    row = 0
    col = 1

    for reliability,cost in zip(reliabilities,costs):
        edge_list.append(Edge(city_list[row],city_list[col],float(cost),float(reliability)))
        if(col == len(city_list)-1):
            row = row+1
            col = row+1
        else:
            col= col+1
    return city_list, edge_list