import datetime
import os
import pandas as pd
from pathlib import Path
import ast


def convert_csv_column_to_list(filename):
    dataframe = pd.DataFrame(pd.read_csv(filename))
    return list(dataframe['Kmer'])


def add_kmer(dict, kmer):
    if not kmer[0] in dict.keys():
        dict[kmer[0]] = {}

    ptr = dict[kmer[0]]
    itr = 1

    while itr < len(kmer):

        if kmer[itr] not in ptr.keys():
            ptr[kmer[itr]] = {}
        ptr = ptr[kmer[itr]]
        itr += 1


def has_kmer(dict, kmer):
    itr = 0

    if not kmer[0] in dict.keys():
        return False

    ptr = dict[kmer[0]]
    itr = 1

    while itr < len(kmer):

        if kmer[itr] not in ptr.keys():
            return False
        else:
            ptr = ptr[kmer[itr]]
            itr += 1
    return True


def get_child_count(d):
    cnt = 0
    for e in d:
        if d[e] != {}:
            cnt += get_child_count(d[e])
        else:
            cnt += 1
    return cnt


class Summer:
    def __init__(self):
        self.summing = 0


def nested_tree_comparison(dict1, dict2, summ):

    for k in dict1.keys():

        if (k not in dict2.keys()):
            if(dict1[k] == {}):
                summ.summing += 1

            else:
                summ.summing += get_child_count(dict1[k])

        else:
            nested_tree_comparison(dict1[k], dict2[k], summ)


def kmer_distance_main(csv_file_list_path, kmer_forest_path, file_dict):
    CSVFileList = os.listdir(csv_file_list_path)
    CSVFileList.sort()
    specie_list = []
    time1 = datetime.datetime.now()
    print("started at : "+str(time1))
    all_dicts = []
    k_lists = []
    for each_CSV_file in CSVFileList:

        specie_name = each_CSV_file.split('_GCF')[0].split('_kmer')[0]
        print(specie_name, 'forest construction started')
        specie_list.append(specie_name)

        kmer_list = convert_csv_column_to_list(
            csv_file_list_path+each_CSV_file)

        # k_lists.append(kmer_list)
        dict = {}
        time1 = datetime.datetime.now()

        print("Kmer adding Started")
        for each_kmer in kmer_list:
            add_kmer(dict, each_kmer)

        print("KMer addding Finished")

        time2 = datetime.datetime.now()
        print("forest construction finished : "+str(time2-time1))

        txt_f = open(kmer_forest_path + specie_name + ".txt", 'w+')
        txt_f.write(str(dict))
        txt_f.close()
        # all_dicts.append(dict)

        count = 0
        for each_kmer in kmer_list:
            if(has_kmer(dict, each_kmer)):
                count = count+1

    # time23 = datetime.datetime.now()

    # kmer_similarities = ""
    # for i in range(0, len(all_dicts)):
    #     for j in range(i, len(all_dicts)):
    #         summ = Summer()
    #         print('Forest comparison Started ', specie_list[i], specie_list[j])
    #         nested_tree_comparison(all_dicts[i], all_dicts[j], summ)

    #         intersection = (len(k_lists[i]) - summ.summing)
    #         union = (len(k_lists[j]) + summ.summing)

    #         time33 = datetime.datetime.now()
    #         print('Forest comparison Finished')
    #         print('distance', specie_list[i],
    #               specie_list[j], intersection / union)

    #         new_line = file_dict[specie_list[i]] + ',' + \
    #             file_dict[specie_list[j]] + ',' + str(intersection/union)+'\n'
    #         kmer_similarities += new_line
    #         print('Elapsed time for cosmparison', (time33 - time23))
    return True


def readDict(path):
    print(path+" Reading Started!")
    current_file = open(path, "r")
    contents = current_file.read()
    dictionary = ast.literal_eval(contents)
    current_file.close()
    return dictionary


def comparison_of_forests(csv_file_list_path, kmer_forest_path, file_dict):
    time23 = datetime.datetime.now()
    specie_list = []
    k_lists = []

    CSVFileList = os.listdir(csv_file_list_path)
    CSVFileList.sort()

    for each_CSV_file in CSVFileList:

        specie_name = each_CSV_file.split('_GCF')[0].split('_kmer')[0]
        print(specie_name, 'forest construction started')

        kmer_list = convert_csv_column_to_list(
            csv_file_list_path+each_CSV_file)

        k_lists.append(kmer_list)

    print("KMer List Appending Finished")
    SpeciesFileList = os.listdir(kmer_forest_path)
    SpeciesFileList.sort()

    for path in SpeciesFileList:
        specie_list.append(path.split(".")[0])

    kmer_similarities = ""

    for i in range(0, len(SpeciesFileList)):
        print(i)
        i_dict = readDict(kmer_forest_path+SpeciesFileList[i])
        for j in range(i, len(SpeciesFileList)):
            j_dict = readDict(kmer_forest_path+SpeciesFileList[j])
            summ = Summer()
            print('Forest comparison Started ',
                  specie_list[i], specie_list[j])
            nested_tree_comparison(i_dict, j_dict, summ)

            intersection = (len(k_lists[i]) - summ.summing)
            union = (len(k_lists[j]) + summ.summing)

            time33 = datetime.datetime.now()
            print('Forest comparison Finished')
            print('distance', specie_list[i],
                  specie_list[j], intersection / union)

            new_line = file_dict[specie_list[i]] + ',' + \
                file_dict[specie_list[j]] + ',' + \
                str(intersection/union)+'\n'
            kmer_similarities += new_line
            print('Elapsed time for cosmparison', (time33 - time23))
    return kmer_similarities
