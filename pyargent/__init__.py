from dataclasses import dataclass
from typing import List, Optional
from injector import Injector, inject

from pyargent.entity.salary import Salary, SalaryTax, SalaryPayment, SalaryDeduction, SalaryRepository
from .di_container import DiS3, DiLocal


# comparable tuple
VERSION = (0, 1, 0)
# generate __version__ via VERSION tuple
__version__ = ".".join(map(str, VERSION))

__all__ = ["py_argent"]


@inject
@dataclass
class PyArgent:
    salary_repository: SalaryRepository

    def save_salary(self, salary: Salary) -> str:
        return self.salary_repository.save(salary=salary)

    def load_salary(self, dt: str) -> List[Salary]:
        return self.salary_repository.load(dt=dt)


def py_argent(storage: str, prefix: str, s3_bucket: Optional[str] = None) -> PyArgent:
    if storage == "s3":
        di = Injector([DiS3(s3_bucket=s3_bucket, prefix=prefix)])
    elif storage == "local":
        di = Injector([DiLocal(prefix=prefix)])
    else:
        raise ValueError()
    return di.get(PyArgent)
