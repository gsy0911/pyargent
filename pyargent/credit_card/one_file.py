from dataclasses import dataclass, field, asdict
import hashlib
from typing import List

import pandas as pd

from .one_row import OneRow


@dataclass(init=True, order=True)
class OneFile:
    raw_text_list: List[str] = field(default_factory=list, repr=False, compare=False)
    one_row_list: List[OneRow] = field(default_factory=list, compare=False)

    @staticmethod
    def from_file_path(file_path: str, encoding="cp932"):
        with open(file_path, mode="r", encoding=encoding) as f:
            text_list = [s for s in f.readlines()]

        one_row_list = [OneRow.from_text(t) for t in text_list]
        one_row_list = [c for c in one_row_list if c is not None]
        return OneFile(raw_text_list=text_list, one_row_list=one_row_list)

    @staticmethod
    def from_file_path_list(file_path_list: List[str], encoding="cp932"):
        whole_raw_text_list = []
        whole_one_row_list = []

        for file_path in file_path_list:
            one_file = OneFile.from_file_path(file_path, encoding)
            whole_raw_text_list.extend(one_file.raw_text_list)
            whole_one_row_list.extend(one_file.one_row_list)
        return OneFile(raw_text_list=whole_raw_text_list, one_row_list=whole_one_row_list)

    def _to_df(self) -> pd.DataFrame:
        replace_dict = {"total_billing": "", "count": "", "num": "", "actual_billing": ""}
        astype_dict = {
            "total_billing": "int",
            "count": "int",
            "num": "int",
            "actual_billing": "int"
        }
        return pd.DataFrame([asdict(c) for c in self.one_row_list]) \
            .replace(replace_dict, "0") \
            .astype(astype_dict)

    @staticmethod
    def _add_group(_df: pd.DataFrame) -> pd.DataFrame:
        def to_hash(input_str: str) -> str:
            return hashlib.sha3_256(input_str[:4].encode("cp932")).hexdigest()[:10]

        def get_max_index(same_strings_list: List[str]) -> int:
            """

            Args:
                same_strings_list:

            Returns:

            Examples:
                >>> _input = [
                >>>     "some_string_4214", "some_string_9951", "some_string_9041"
                >>> ]
                >>> get_max_index(_input)
                len("some_string_")


            """
            max_length = max([len(s) for s in same_strings_list])
            max_index = 0
            for i in range(max_length):
                strings_starts_list = [s[:i + 1] for s in same_strings_list]
                strings_set = set(strings_starts_list)
                if len(strings_set) == 1:
                    max_index = i + 1
                else:
                    break
            return max_index

        def get_max_same_string(same_strings_list: List[str]) -> str:
            """

            Args:
                same_strings_list:

            Returns:

            Examples:
                >>> _input = [
                >>>     "some_string_4214", "some_string_9951", "some_string_9041"
                >>> ]
                >>> get_max_same_string(_input)
                "some_string_"

            """
            max_index = get_max_index(same_strings_list)
            return same_strings_list[0][:max_index]

        # add hash column
        _df['hash'] = _df['description'].apply(to_hash)
        hash_dict = {}
        for _hash, g_df in _df.groupby("hash"):
            description_list = list(g_df['description'].drop_duplicates().values)

            group = get_max_same_string(description_list)
            hash_dict[_hash] = {
                "hash": _hash,
                "group": group
            }
        hash_df = pd.DataFrame.from_dict(hash_dict, orient="index")
        return pd.merge(_df, hash_df, on="hash", how="inner").drop("hash", axis=1)

    @staticmethod
    def _df_split_date(_df) -> pd.DataFrame:
        ymd_df = pd.DataFrame(list(_df['date'].apply(lambda x: x.split("/"))), columns=["year", "month", "day"])
        _df[['year', 'month', 'day']] = ymd_df
        return _df

    def to_df(self, add_group=True, split_date=True) -> pd.DataFrame:
        df = self._to_df()
        if add_group:
            df = self._add_group(_df=df)
        if split_date:
            df = self._df_split_date(_df=df)
        return df
