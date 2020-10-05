import pulp
import pandas as pd
import numpy as np


def solver(target, bag, budget):
    """
    Solver Function To Build Media Plan from expected KPI's and total campaign budget

    :param target: Which metrics is supposed to be optmized. It can be:
    * CPM - Cost per Thousand Impressions
    * CPC - Cost per click
    * CPV - Cost per visits
    * CPA - Cost per acquisition

    :param bag: Dictionary containing all expected performance metrics

    Must attend the following structure

    bag = {'spendCap': {channel: value for channel in channel set},
           'channelType': {channel: cat for channel in channel set},
           'CPM': {channel: value for channel in channel set},
           'CPC': {channel: value for channel in channel set},
           'CPC': {channel: value for channel in channel set},
           'CPA': {channel: value for channel in channel set}
           }

    :param budget: Total Campaign Budget
    :return: DataFrame with Optimal Budget Allocation
    """

    # Building The Model
    model = pulp.LpProblem("maximize_{}".format(target), pulp.LpMaximize)
    # Dict with Model Variables
    mvar = {}
    for name in bag[target].keys():
        if bag['channelType'][name] == 'tb':
            mvar.update({name: pulp.LpVariable(name, lowBound=0, cat='Integer')})
        else:
            mvar.update({name: pulp.LpVariable(name, lowBound=0, cat='Continuous')})
    # Incrementing Objective Function
    model += sum([mvar[name] * (bag[target][name] ** -1) for name in mvar.keys()])
    # Model Constraints - Total Budget
    model += sum([mvar[name] for name in mvar.keys()]) == budget
    # Model Constraints - Spending Capability per Channel
    for name in mvar.keys():
        model += mvar[name] <= bag['spendCap'][name]

    status = model.solve()

    if pulp.LpStatus[status] == 'Optimal':
        # Bulding Media Plan
        mp = pd.DataFrame.from_dict([{'optimal_budget': pulp.value(mvar[name]),
                                      'channel': name} for name in mvar.keys()])
        # Mapping All Plan Metrics
        mp['CPM'] = mp['channel'].map(bag['CPM'])
        mp['CPC'] = mp['channel'].map(bag['CPC'])
        mp['CPV'] = mp['channel'].map(bag['CPV'])
        mp['CPA'] = mp['channel'].map(bag['CPA'])

        mp['impressions'] = np.round((mp['optimal_budget'] * 1000) / mp['channel'].map(bag['CPM']), 0)
        mp['clicks'] = np.round(mp['optimal_budget'] / mp['channel'].map(bag['CPC']), 0)
        mp['visits'] = np.round(mp['optimal_budget'] / mp['channel'].map(bag['CPV']), 0)
        mp['conversions'] = np.round(mp['optimal_budget'] / mp['channel'].map(bag['CPA']), 0)

        mp.set_index('channel', inplace=True)
        mp.index.name = 'channel'

        return mp
    else:
        return {'error_01': 'unable to converge model'}
