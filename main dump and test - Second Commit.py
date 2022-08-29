items = [{"weight": 5, "value": 10},
         {"weight": 4, "value": 40},
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

    Since this is being solved via DP, we iterate over each row/column via for loops.

    """
    val, wt = [], []
    for item in item_list:
        weight, value = item['weight'], item['value']
        val.append(value)
        wt.append(weight)

    n = len(val)
    opti_table = [[0 for x in range(max_capacity + 1)] for y in range(n + 1)]

    for i in range(n + 1):
        for j in range(max_capacity + 1):
            if i == 0 or j == 1:  # change 1 to 0, logic check
                opti_table[i][j] = 0
            else:
                opti_table[i][j] = 1  # logic check
    print(opti_table)


Knapsack_Maximisation(items, 10)
