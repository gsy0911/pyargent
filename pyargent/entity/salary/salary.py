from dataclasses import dataclass, field


@dataclass(frozen=True)
class SalaryPayment:
    basic_payment: int = field(default_factory=int, metadata={"jp": "基本給"})
    overtime_fee: int = field(default_factory=int, metadata={"jp": "残業代"})
    static_overtime_fee: int = field(default_factory=int, metadata={"jp": "固定残業代"})
    commuting_fee: int = field(default_factory=int, metadata={"jp": "通勤（非課税）"})

    def total(self):
        return sum(self.__dict__.values())

    def taxable(self):
        return sum([
            self.basic_payment,
            self.overtime_fee,
            self.static_overtime_fee
        ])

    @staticmethod
    def from_dict(data: dict):
        _data = {k: v for k, v in data.items() if k in SalaryPayment.__dataclass_fields__.keys()}
        return SalaryPayment(**_data)


@dataclass(frozen=True)
class SalaryDeduction:
    health_insurance: int = field(default_factory=int, metadata={"jp": "健康保険"})
    nursing_insurance: int = field(default_factory=int, metadata={"jp": "介護保険"})
    welfare_pension: int = field(default_factory=int, metadata={"jp": "厚生年金"})
    pension_fund: int = field(default_factory=int, metadata={"jp": "年金基金"})
    welfare_pension: int = field(default_factory=int, metadata={"jp": "雇用保険"})

    def total(self):
        return sum(self.__dict__.values())

    @staticmethod
    def from_dict(data: dict):
        _data = {k: v for k, v in data.items() if k in SalaryDeduction.__dataclass_fields__.keys()}
        return SalaryDeduction(**_data)


@dataclass(frozen=True)
class SalaryTax:
    income_tax: int = field(default_factory=int, metadata={"jp": "源泉所得税"})
    resident_tax: int = field(default_factory=int, metadata={"jp": "住民税"})
    year_end_tax_adjustment: int = field(default_factory=int, metadata={"jp": "年末調整"})

    def total(self):
        return sum(self.__dict__.values())

    @staticmethod
    def from_dict(data: dict):
        _data = {k: v for k, v in data.items() if k in SalaryTax.__dataclass_fields__.keys()}
        return SalaryTax(**_data)


@dataclass(frozen=True)
class Salary:
    version: str = field(default_factory=str, metadata={"jp": "版"})
    payment_date: str = field(default_factory=str, metadata={"jp": "支給日"})
    calc_start_date: str = field(default_factory=str, metadata={"jp": "計算開始日"})
    calc_end_date: str = field(default_factory=str, metadata={"jp": "計算締め日"})
    salary_payment: SalaryPayment = field(default_factory=SalaryPayment, metadata={"jp": "給与"})
    salary_deduction: SalaryDeduction = field(default_factory=SalaryDeduction, metadata={"jp": "保険"})
    salary_tax: SalaryTax = field(default_factory=SalaryTax, metadata={"jp": "所得税など"})

    @staticmethod
    def from_dict(data: dict):
        _data = {k: v for k, v in data.items() if k in ["payment_date", "calc_start_date", "calc_end_date"]}
        _data.update({
            "salary_payment": SalaryPayment.from_dict(data),
            "salary_deduction": SalaryDeduction.from_dict(data),
            "salary_tax": SalaryTax.from_dict(data)
        })
        return Salary(**_data)

    @staticmethod
    def of():
        pass
