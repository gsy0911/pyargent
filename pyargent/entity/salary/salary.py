from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List


@dataclass(frozen=True)
class SalaryPayment:
    basic_payment: int = field(default_factory=int, metadata={"jp": "基本給"})
    overtime_fee: int = field(default_factory=int, metadata={"jp": "残業代"})
    static_overtime_fee: int = field(default_factory=int, metadata={"jp": "固定残業代"})
    commuting_fee: int = field(default_factory=int, metadata={"jp": "通勤（非課税）"})
    additional_allowance: int = field(default_factory=int, metadata={"jp": "その他手当"})

    def total(self):
        return sum(self.__dict__.values())

    def taxable(self):
        return sum([self.basic_payment, self.overtime_fee, self.static_overtime_fee])

    @staticmethod
    def loads(data: dict):
        _data = {k: v for k, v in data.items() if k in SalaryPayment.__dataclass_fields__.keys()}
        return SalaryPayment(**_data)

    def dumps(self):
        return asdict(self)


@dataclass(frozen=True)
class SalaryDeduction:
    health_insurance: int = field(default_factory=int, metadata={"jp": "健康保険"})
    nursing_insurance: int = field(default_factory=int, metadata={"jp": "介護保険"})
    welfare_pension: int = field(default_factory=int, metadata={"jp": "厚生年金"})
    pension_fund: int = field(default_factory=int, metadata={"jp": "年金基金"})
    employment_insurance: int = field(default_factory=int, metadata={"jp": "雇用保険"})

    def total(self):
        return sum(self.__dict__.values())

    @staticmethod
    def loads(data: dict):
        _data = {k: v for k, v in data.items() if k in SalaryDeduction.__dataclass_fields__.keys()}
        return SalaryDeduction(**_data)

    def dumps(self):
        return asdict(self)


@dataclass(frozen=True)
class SalaryTax:
    income_tax: int = field(default_factory=int, metadata={"jp": "源泉所得税"})
    inhabitant_tax: int = field(default_factory=int, metadata={"jp": "住民税"})
    year_end_tax_adjustment: int = field(default_factory=int, metadata={"jp": "年末調整"})

    def total(self):
        return sum(self.__dict__.values())

    @staticmethod
    def loads(data: dict):
        _data = {k: v for k, v in data.items() if k in SalaryTax.__dataclass_fields__.keys()}
        return SalaryTax(**_data)

    def dumps(self):
        return asdict(self)


@dataclass(frozen=True)
class Salary:
    payment_date: str = field(default=str, metadata={"jp": "支給日"})
    calc_start_date: str = field(default=str, metadata={"jp": "計算開始日"})
    calc_end_date: str = field(default=str, metadata={"jp": "計算締め日"})
    salary_payment: SalaryPayment = field(default_factory=SalaryPayment, metadata={"jp": "給与"})
    salary_deduction: SalaryDeduction = field(default_factory=SalaryDeduction, metadata={"jp": "保険"})
    salary_tax: SalaryTax = field(default_factory=SalaryTax, metadata={"jp": "所得税など"})
    company: str = field(default=str, metadata={"jp": "所得税など"})
    version: str = field(default="1", metadata={"jp": "版"})

    @staticmethod
    def loads(data: dict):
        _data = {k: v for k, v in data.items() if k in ["payment_date", "calc_start_date", "calc_end_date"]}
        _data.update(
            {
                "salary_payment": SalaryPayment.loads(data.get("salary_payment", {})),
                "salary_deduction": SalaryDeduction.loads(data.get("salary_deduction", {})),
                "salary_tax": SalaryTax.loads(data.get("salary_tax", {})),
            }
        )
        return Salary(**_data)

    def dumps(self):
        return asdict(self)

    def total_payments(self) -> int:
        """
        総支給額

        Returns:

        """
        return self.salary_payment.total()

    def total_deductions(self) -> int:
        """
        控除額合計

        Returns:

        """
        return self.salary_deduction.total() + self.salary_tax.total()

    def net_payment(self) -> int:
        """
        差引支給額

        Returns:

        """
        return self.total_payments() - self.total_deductions()

    def dt(self) -> str:
        return datetime.strptime(self.payment_date, "%Y-%m-%d").strftime("%Y_%m")

    @staticmethod
    def of(
        company: str,
        payment_date: str,
        calc_start_date: str,
        calc_end_date: str,
        basic_payment: int,
        overtime_fee: int,
        static_overtime_fee: int,
        commuting_fee: int,
        additional_allowance: int,
        health_insurance: int,
        nursing_insurance: int,
        welfare_pension: int,
        pension_fund: int,
        employment_insurance: int,
        income_tax: int,
        inhabitant_tax: int,
        year_end_tax_adjustment: int,
    ) -> "Salary":
        salary_payment = SalaryPayment(
            basic_payment=basic_payment,
            overtime_fee=overtime_fee,
            static_overtime_fee=static_overtime_fee,
            commuting_fee=commuting_fee,
            additional_allowance=additional_allowance
        )

        salary_deduction = SalaryDeduction(
            health_insurance=health_insurance,
            nursing_insurance=nursing_insurance,
            welfare_pension=welfare_pension,
            pension_fund=pension_fund,
            employment_insurance=employment_insurance,
        )

        salary_tax = SalaryTax(
            income_tax=income_tax, inhabitant_tax=inhabitant_tax, year_end_tax_adjustment=year_end_tax_adjustment
        )

        return Salary(
            company=company,
            payment_date=payment_date,
            calc_start_date=calc_start_date,
            calc_end_date=calc_end_date,
            salary_payment=salary_payment,
            salary_deduction=salary_deduction,
            salary_tax=salary_tax,
        )


@dataclass(frozen=True)
class SalaryRepository(metaclass=ABCMeta):
    @staticmethod
    def file_name(salary: Salary) -> str:
        return f"{salary.dt()}_{salary.company}.json"

    @abstractmethod
    def path(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def save(self, salary: Salary):
        raise NotImplementedError

    @abstractmethod
    def load(self, dt: str) -> List[Salary]:
        raise NotImplementedError
