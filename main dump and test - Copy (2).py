from tabulate import tabulate

items = [{"weight": 1, "value": 10},
         {"weight": 2, "value": 40},
         {"weight": 6, "value": 30},
         {"weight": 4, "value": 50}]


def Knapsack_Maximisation(item_list, max_capacity):
    """The knapsack problem is a mainstay of the optimisation field.
    Here, we aim to maximise the amount of items that can fit into knapsack.
    There are various methods of solving this problem, this function focuses
    on the dynamic programming (DP) approach using a table.

    The function takes the parameters item_list and max_capacity; where
    max_capacity is the maximum capacity of the knapsack whilst item_list is
    a list of dictionaries that contain "weight" and "value" as key:value pairs
    for each item.

    Initially, the item_list is split into two distinct lists that are returned
    as wt and val:
    wt is the weight of each item
    val is the value of each item.

    Then, an (optimisation) table of the dimensions [[max_capacity+1][n+1]] is made.
    Here "n" is the total number of items.
    We add +1 to both max_capacity and n because we need to account for the "0" column and row.

    Since this is being solved via DP, we iterate over each row/column via for-loops and manipulate
    the values therein (since the table was initialised with 0's throughout).



    """
    val, wt = [], []
    for item in item_list:
        weight, value = item['weight'], item['value']
        val.append(value)
        wt.append(weight)

    n = len(val)  # item count
    opti_table = [[0 for x in range(max_capacity + 1)] for y in range(n + 1)]
    counter = 1
    for i in range(n + 1):  # for every row (1 per item + 1)
        counter = counter +1
        for j in range(max_capacity + 1):  # for every column of that row (each column = incremental to maximum weight +1)
            counter = counter +1
            if i == 0 or j == 0:
                opti_table[i][j] = 0  # set 0 for first row/column
            elif wt[i - 1] <= j:  # if the previous item's weight is <= the current max_capacity (j) then:
                opti_table[i][j] = max(val[i - 1] + opti_table[i - 1][j - wt[i - 1]], opti_table[i - 1][j])
                # returning max value of either
                # (value of the previous item + value at opti_table[previous item][max_current_capacity - wt(i-1)]
                # in the example of items 1&2 being wt 1,2,3 and val of 10,40,30:
                # at iteration 48 for sanity checking:
                print(f"i:{i}, j:{j}, Iteration: {counter}")
                print(f"{val[i - 1]} + {opti_table[i - 1][j - wt[i - 1]]} | previous value coordinates are - row:[{i - 1}] & column:[{j - wt[i - 1]}]")
                #results in:
                #i:3, j:9, Iteration: 48
                #30 + 50 | previous value coordinates are - row:[2] & column:[3]
                #so new value is 80, confirmed
                print(tabulate(opti_table))
            else:
                opti_table[i][j] = 0  # logic check

    #print(tabulate(opti_table))
    print(opti_table[n][max_capacity])



Knapsack_Maximisation(items, 10)
