def bagchecker(bag):

    # Check if bag is a dictionary
    if isinstance(bag, dict):

        # Already Asserted as Key - Sorting Keys
        a = list(bag.keys())
        a.sort()
        # Model Required Bag Keys
        keys = ['CPA', 'CPC', 'CPM', 'CPV', 'channelType', 'spendCap']
        # Check all necessary keys are in bag
        if a == keys:
            # Fetching Channels
            channels_a = list(bag['spendCap'].keys())
            channels_b = list(bag['channelType'].keys())

            # Sorting lists
            channels_a.sort()
            channels_b.sort()

            if channels_a == channels_b:
                return {'results': 'ok', 'message': 'all god!'}
            else:
                missing_channels = [ch for ch in set(channels_a + channels_b) if ch not in list(set(channels_a) & set(channels_b))]
                return {'results': 'fail', 'message': ", ".join(missing_channels) + "Channels are missing in the bag parameter."}
        else:
            missing_keys = [key for key in a if key not in keys]
            return {'results': 'fail', 'message': ", ".join(missing_keys) + "Keys are missing in the bag parameter."}
    else:
        return {'results': 'fail', 'message': "pbag must be a dictionary with specific design"}
