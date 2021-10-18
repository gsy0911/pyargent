from dataclasses import dataclass
import json
from typing import List

import s3fs

from pyargent.entity.salary import Salary, SalaryRepository


@dataclass(frozen=True)
class SalaryS3(SalaryRepository):
    s3_bucket: str
    prefix: str
    fs = s3fs.S3FileSystem(anon=False)

    def path(self):
        return f"{self.s3_bucket}/{self.prefix}"

    def save(self, salary: Salary):
        path = f"{self.path}/{self.file_name(salary=salary)}"
        with self.fs.open(path, "w") as f:
            json.dump(salary.dumps, f)

    def load(self, dt: str) -> List[Salary]:
        path_candidate = f"{self.path}/{dt}*"
        file_list = self.fs.glob(path_candidate)
        print(file_list)
        return []


@dataclass(frozen=True)
class SalaryLocal(SalaryRepository):
    prefix: str

    def path(self):
        return self.prefix

    def save(self, salary: Salary):
        raise NotImplementedError

    def load(self, dt: str) -> List[Salary]:
        raise NotImplementedError
