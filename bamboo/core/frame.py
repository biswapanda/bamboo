from pandas import DataFrame, Series

from bamboo.lib.jsontools import series_to_jsondict
from bamboo.lib.mongo import dump_mongo_json


# reserved bamboo keys
BAMBOO_RESERVED_KEY_PREFIX = 'BAMBOO_RESERVED_KEY_'
DATASET_ID = BAMBOO_RESERVED_KEY_PREFIX + 'dataset_id'
DATASET_OBSERVATION_ID = BAMBOO_RESERVED_KEY_PREFIX + 'dataset_observation_id'
PARENT_DATASET_ID = BAMBOO_RESERVED_KEY_PREFIX + 'parent_dataset_id'
BAMBOO_RESERVED_KEYS = [
    DATASET_ID,
    DATASET_OBSERVATION_ID,
    PARENT_DATASET_ID,
]


class BambooFrame(DataFrame):
    def add_parent_column(self, parent_dataset_id):
        column = Series([parent_dataset_id] * len(self))
        column.name = PARENT_DATASET_ID
        return self.__class__(self.join(column))

    def remove_bamboo_reserved_keys(self, keep_parent_ids=False):
        reserved_keys = list(set(BAMBOO_RESERVED_KEYS).intersection(
            set(self.columns.tolist())))
        if keep_parent_ids and PARENT_DATASET_ID in reserved_keys:
            reserved_keys.remove(PARENT_DATASET_ID)
        for column in reserved_keys:
            del self[column]

    def to_jsondict(self):
        return [series_to_jsondict(series) for idx, series in self.iterrows()]

    def to_json(self):
        """
        Convert mongo *cursor* to json dict, via dataframe, then dump to JSON.
        """
        jsondict = self.to_jsondict()
        return dump_mongo_json(jsondict)
