from dataclasses import dataclass, field, asdict
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

    def to_df(self) -> pd.DataFrame:
        df = pd.DataFrame([asdict(c) for c in self.one_row_list])
        df = df.replace({"total_billing": "", "count": "", "num": "", "actual_billing": ""}, "0")
        df = df.astype({
            "total_billing": "int",
            "count": "int",
            "num": "int",
            "actual_billing": "int"
        })
        return df
