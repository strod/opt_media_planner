from solver import solver
from bag_checker import bagchecker


class MediaPlanner:
    def __init__(self, bag, data=None):
        """

        :param bag: Dictionary containing all expected performance metrics

        Must attend the following structure

        bag = {'spendCap': {channel: value for channel in channel set},
               'channelType': {channel: cat for channel in channel set},
               'CPM': {channel: value for channel in channel set},
               'CPC': {channel: value for channel in channel set},
               'CPC': {channel: value for channel in channel set},
               'CPA': {channel: value for channel in channel set}
               }

        :param data: Historical Data
        """
        # Validations:
        results = bagchecker(bag)

        if results['results'] == 'ok':
            pass
        else:
            raise ValueError("{0}".format(results['message']))

        # Defining Media Plan Attributes
        self.channels = list(bag['spendCap'].keys())

        # Bag of KPI''
        self.bag = bag

        # Historical Data
        if data is None:
            pass
        else:
            self.data = data

    def generate_plan(self, budget, target='CPA'):
        """

        :param target:
        :param budget:
        :return:
        """
        return solver(target=target, bag=self.bag, budget=budget)
