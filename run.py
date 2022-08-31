
from flask import Flask, render_template, url_for, request
import csv
import os
import io

app = Flask(__name__)
def getFromCsvFile(fname):
    loopSets = []
    loopSet = set()

    s = io.StringIO(fname.stream.read().decode("UTF8"), newline=None)
    cRead = reader(s)
    for cell in cRead:
            cell = list(filter(None,cell))
            data = set(cell)
            for item in data:
                loopSet.add(frozenset([item]))
            loopSets.append(data)
    return(loopSet, loopSets)


minsup = 20
f2 = "Rules.txt"
f1 = "FItems.txt"
minconf = 0.39


def L1(data):
    '''
    Find frequent 1-itemsets
    '''
    #Get all 1-itemsets in the list items and their counts in the dictionary counts
    s = io.StringIO(data.stream.read().decode("UTF8"), newline=None)
    DataCaptured = csv.reader(s, delimiter=',')
    data = list(DataCaptured)
    for e in data:
        e = sorted(e)
    count = {}
    for items in data:
        for item in items:
            if item not in count:
                count[(item)] = 1
            else:
                count[(item)] = count[(item)] + 1
    #print("C1 Items", count)
    # print("C1 Length : ", len(count))
    # print(count)

    #Thresholding
    count2 = {k: v for k, v in count.items() if v >= minsup}
    #print("L1 Items : ", count2)
    # print("L1 Length : ", len(count2))
    # print()

    return count2, data


def generateCk(Lk_1, flag, data):
    '''
    Generate Ck by joining 2 Lk-1
    '''
    Ck = []

    if flag == 1:
        flag = 0
        for item1 in Lk_1:
            for item2 in Lk_1:
                if item2 > item1:
                    Ck.append((item1, item2))
        # print("C2: ", Ck)
        # print("length : ", len(Ck))
        # print()

    else:
        for item in Lk_1:
            k = len(item)
        for item1 in Lk_1:
            for item2 in Lk_1:
                if (item1[:-1] == item2[:-1]) and (item1[-1] != item2[-1]):
                    if item1[-1] > item2[-1]:
                        Ck.append(item2 + (item1[-1],))
                    else:
                        Ck.append(item1 + (item2[-1],))
        # print("C" + str(k+1) + ": ", Ck[1:3])
        # print("Length : ", len(Ck))
        # print()
    L = generateLk(set(Ck), data)
    return L, flag


def generateLk(Ck, data):
    '''
    If item in Ck belongs to a transaction,
    it makes it into list Ct
    Then Ct is thresholded to form L
    '''
    count = {}
    for itemset in Ck:
        #print(itemset)
        for transaction in data:
            if all(e in transaction for e in itemset):
                if itemset not in count:
                    count[itemset] = 1
                else:
                    count[itemset] = count[itemset] + 1

    # print("Ct Length : ", len(count))
    # print()

    count2 = {k: v for k, v in count.items() if v >= minsup}
    # print("L Length : ", len(count2))
    # print()
    return count2


def apriori(data):
    L, data = L1(data)
    flag = 1
    allItems = dict(L)
    while(len(L) != 0):
        fo = open(f1, "a+")
        for k, v in L.items():
            fo.write(str(k) + ' >>> ' + str(v) + '\n\n')
        fo.close()

        L, flag = generateCk(L, flag, data)
        allItems.update(L)
        norm = {}
        for k, vals in allItems.items():
            # print(vals)
            values = []
            norm[k] = values
        updateItems = []
        for string in norm:
            updateItems.append(string)
    print(updateItems)
    return updateItems  



@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/result',methods=['POST', 'GET'])
def result():
    output = request.files['myfile']
    op = apriori(output)
    # f1, rules = aprioriFromCsvFile(output,20)
    return render_template('index.html', temp = op)
    
if __name__ == "__main__":
    app.run(debug=True)