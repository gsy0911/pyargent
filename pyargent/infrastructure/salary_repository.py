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
        return f"s3://{self.s3_bucket}/{self.prefix}"

    def save(self, salary: Salary) -> str:
        path = f"{self.path()}/{self.file_name(salary=salary)}"
        with self.fs.open(path, "w") as f:
            json.dump(salary.dumps(), f)
        return path

    def load(self, dt: str) -> List[Salary]:
        path_candidate = f"{self.path()}/{dt.replace('-', '_')}*"
        path_list = self.fs.glob(path_candidate)

        salary_list = []
        for path in path_list:
            print(path)
            with self.fs.open(path, "r") as f:
                data = json.load(f)
                salary_list.append(Salary.loads(data=data))
        return salary_list


@dataclass(frozen=True)
class SalaryLocal(SalaryRepository):
    prefix: str

    def path(self):
        return self.prefix

    def save(self, salary: Salary):
        path = f"{self.path()}/{self.file_name(salary=salary)}"
        with open(path, "w") as f:
            json.dump(salary.dumps(), f)

    def load(self, dt: str) -> List[Salary]:
        path_candidate = f"{self.path()}/{dt}*"
        return []
