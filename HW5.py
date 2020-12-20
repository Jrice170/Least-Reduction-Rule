import numpy as np
import pandas as pd

from statsmodels.stats.proportion import proportion_confint



df = pd.read_csv("breast-cancer.csv")
print(df.age.value_counts(ascending=True))



def Data_slicer(data_fame,logic_string,atribute_string,value):

        logic_operator_str = logic_string
        if(logic_string == "<"):

            return df.loc[df[atribute_string] < value,:]
        elif(logic_string == "<="):

            return df.loc[df[atribute_string] <= value,:]
        elif(logic_string=='>'):

            return df.loc[df[atribute_string] > value,:]

        elif(logic_string == ">="):

            return df.loc[df[atribute_string] >= value,:]

        elif(logic_string == "=="):

            return df.loc[df[atribute_string] == value,:]

        elif(logic_string == "!="):
            return df.loc[df[atribute_string] != value,:]

#logical intersection of a set of subsets in data_fram
def merge_frames(Data_list_frame22):

    List_size_22 = len(Data_list_frame22)
    New_data_frame = pd.merge(Data_list_frame22[0],Data_list_frame22[1],how= 'inner')

    for i in range(2,List_size_22):
        New_data_frame = pd.merge(New_data_frame,Data_list_frame22[i],how='inner')

    return New_data_frame

Test_list = [[0,1,420],[5,2,0.5],[16,2,250],[21,4,2]]
"""
test_1 = df.loc[df.age=='40-49',:]
test_2 = df.loc[df["tumor-size"]=='0-4',:]
test_3 = df.loc[df["inv-nodes"]=='0-2',:]
test_4 = df.loc[df["node-caps"]=='no',:]
"""

test_1 = Data_slicer(df,'!=',"tumor-size",'0-4')

test_2 = Data_slicer(df,'==','age','40-49')
print(test_2)
test_3 = Data_slicer(df,'==',"inv-nodes",'0-2')
##print(test_3)
test_4 = Data_slicer(df,"==","node-caps",'no')
##print(test_4)
test_5 = Data_slicer(df,"==","Class","no-recurrence-events")


F = [test_1,test_2,test_3,test_4,test_5]




V = pd.merge(test_1,test_2,how='inner')
C  = pd.merge(V,test_3,how='inner')
B = pd.merge(C,test_4,how='inner')
N = pd.merge(B,test_5,how= 'inner')
print(N)












def rule_optimised(data_fram,rule,confidence_level=0.5):

    Logic_regular =  ["<","<=",">",">=","==","!="]
    Nagated_logic = [">=",">","<=","<",'!=','==']

    atribute_list = list(data_fram.columns)
    Count_instants = pd.DataFrame(columns = ["Y1","Y2","E1","E2"])
    list_e  = []   #atribute list for data_fram

    for atributes in data_fram:

        list_e.append(atributes)



    length_of_rule = len(rule)
    consiquence_index = rule[length_of_rule-1]

    Atrubutes_in_rule = []


    for each_atrubute in rule:
        Atrubutes_in_rule.append(list_e[each_atrubute[0]])

    Count_instants = pd.DataFrame(columns = ["Y1","Y2","E1","E2","Predicted Error Before","Predicted Error After"],index = Atrubutes_in_rule)

    #Count_instants.index = Atrubutes_in_rule   #### makes row indexs for contigency table





    for atrubute_in_Contin in Count_instants.index:

            Y_data_fram_list = []
            E_data_fram_list = []
            count_1 = 0
             ## starting at nagative not aticidene is nigated first round
            for each in rule:



                if (count_1 == length_of_rule - 1):   ## hits consiquent index

                    E_data_fram_list.append(Data_slicer(data_fram,Nagated_logic[each[1]],list_e[each[0]],each[2]))

                else:

                    E_data_fram_list.append(Data_slicer(data_fram,Logic_regular[each[1]],list_e[each[0]],each[2]))

                Y_data_fram_list.append(Data_slicer(data_fram,Logic_regular[each[1]],list_e[each[0]],each[2]))

                count_1 = count_1 + 1  # keeps track of index of rule




            DATA_FRAME33 = merge_frames(Y_data_fram_list)
            DATA_FRAME332 = merge_frames(E_data_fram_list)

            Count_instants.loc[atrubute_in_Contin,"Y1"] = DATA_FRAME33.index.size



            Count_instants.loc[atrubute_in_Contin,"E1"] = DATA_FRAME332.index.size



    count_2 = 0
    for atrubute_in_Contin in Count_instants.index:

           Y_data_fram_list = []
           E_data_fram_list = []
           count_1 = 0
                  ## starting at nagative not aticidene is nigated first round
           for each in rule:

                if(count_1 != count_2):

                     if (count_1 == length_of_rule - 1):   ## hits consiquent index

                         E_data_fram_list.append(Data_slicer(data_fram,Nagated_logic[each[1]],list_e[each[0]],each[2]))

                     else:

                         E_data_fram_list.append(Data_slicer(data_fram,Logic_regular[each[1]],list_e[each[0]],each[2]))

                     Y_data_fram_list.append(Data_slicer(data_fram,Logic_regular[each[1]],list_e[each[0]],each[2]))

                     count_1 = count_1 + 1  # keeps track of index of rule
                else:


                     if (count_1 == length_of_rule - 1):   ## hits consiquent index

                         E_data_fram_list.append(Data_slicer(data_fram,Nagated_logic[each[1]],list_e[each[0]],each[2]))

                     else:

                         E_data_fram_list.append(Data_slicer(data_fram,Nagated_logic[each[1]],list_e[each[0]],each[2]))

                     Y_data_fram_list.append(Data_slicer(data_fram,Nagated_logic[each[1]],list_e[each[0]],each[2]))

                     count_1 = count_1 + 1  # keeps track of index of rule

           count_2 = count_2 + 1




           DATA_FRAME33 = merge_frames(Y_data_fram_list)
           DATA_FRAME332 = merge_frames(E_data_fram_list)


           Count_instants.loc[atrubute_in_Contin,"Y2"] = DATA_FRAME33.index.size
           Count_instants.loc[atrubute_in_Contin,"E2"] = DATA_FRAME332.index.size


    for i in Count_instants.index:
        Y1 = Count_instants.loc[i,"Y1"]
        E1 = Count_instants.loc[i,"E1"]
        Y2 = Count_instants.loc[i,"Y2"]
        E2 = Count_instants.loc[i,"E2"]
        first1,second2 =proportion_confint(Y1,Y1+E1,alpha=1-confidence_level,method = "beta")
        first2,second2 = proportion_confint(Y1+Y2,Y1+Y2+E2+E1,alpha=1-confidence_level,method = "beta")

        Count_instants.loc[i,"Predicted Error Before"] = first1
        Count_instants.loc[i,"Predicted Error After"] = first2

    #print(Count_instants)
    Count_instants = Count_instants.loc[Count_instants["Predicted Error Before"] < Count_instants["Predicted Error After"],:]

    Rule_hash= []
    for i in Count_instants.index:
        Rule_hash.append(i)

    New_rule_list = []
    for i in Rule_hash:
        for j in rule:

            if(atribute_list[j[0]]==i):
                New_rule_list.append(j)


    #New_rule_list.append(rule[consiquence_index])
    New_rule_list.append(rule[len(rule)-1])

    return New_rule_list



#print("original ")
RULES = [[2,4,"0-4"],[0,4,"40-49"],[4,4,"no"],[3,4,"0-2"],[9,4,"no-recurrence-events"]]
#print(RULES)

Reduced = rule_optimised(df,RULES,0.25)
##print("output reduced: 0.25 coff ")
##print(Reduced)

RULES1 = [[4,4,'no'],[3,4,'0-2'],[2,4,'30-34'],[5,4,3],[8,4,'no'],[7,4,'central'],[9,4,"recurrence-events"]]
B = rule_optimised(df,RULES1,0.90)
print(B)
