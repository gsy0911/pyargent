from pyargent.entity.salary import Salary, SalaryTax, SalaryPayment, SalaryDeduction


# comparable tuple
VERSION = (0, 1, 0)
# generate __version__ via VERSION tuple
__version__ = ".".join(map(str, VERSION))
