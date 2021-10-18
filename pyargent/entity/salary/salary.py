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
        return sum([self.basic_payment, self.overtime_fee, self.static_overtime_fee])

    @staticmethod
    def loads(data: dict):
        _data = {k: v for k, v in data.items() if k in SalaryPayment.__dataclass_fields__.keys()}
        return SalaryPayment(**_data)


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


@dataclass(frozen=True)
class SalaryTax:
    income_tax: int = field(default_factory=int, metadata={"jp": "源泉所得税"})
    resident_tax: int = field(default_factory=int, metadata={"jp": "住民税"})
    year_end_tax_adjustment: int = field(default_factory=int, metadata={"jp": "年末調整"})

    def total(self):
        return sum(self.__dict__.values())

    @staticmethod
    def loads(data: dict):
        _data = {k: v for k, v in data.items() if k in SalaryTax.__dataclass_fields__.keys()}
        return SalaryTax(**_data)


@dataclass(frozen=True)
class Salary:
    payment_date: str = field(default_factory=str, metadata={"jp": "支給日"})
    calc_start_date: str = field(default_factory=str, metadata={"jp": "計算開始日"})
    calc_end_date: str = field(default_factory=str, metadata={"jp": "計算締め日"})
    salary_payment: SalaryPayment = field(default_factory=SalaryPayment, metadata={"jp": "給与"})
    salary_deduction: SalaryDeduction = field(default_factory=SalaryDeduction, metadata={"jp": "保険"})
    salary_tax: SalaryTax = field(default_factory=SalaryTax, metadata={"jp": "所得税など"})
    version: str = field(default="1", metadata={"jp": "版"})

    @staticmethod
    def loads(data: dict):
        _data = {k: v for k, v in data.items() if k in ["payment_date", "calc_start_date", "calc_end_date"]}
        _data.update(
            {
                "salary_payment": SalaryPayment.loads(data),
                "salary_deduction": SalaryDeduction.loads(data),
                "salary_tax": SalaryTax.loads(data),
            }
        )
        return Salary(**_data)

    @staticmethod
    def of(
        payment_date: str,
        calc_start_date: str,
        calc_end_date: str,
        basic_payment: int,
        overtime_fee: int,
        static_overtime_fee: int,
        commuting_fee: int,
        health_insurance: int,
        nursing_insurance: int,
        welfare_pension: int,
        pension_fund: int,
        employment_insurance: int,
        income_tax: int,
        resident_tax: int,
        year_end_tax_adjustment: int,
    ) -> "Salary":
        salary_payment = SalaryPayment(
                basic_payment=basic_payment,
                overtime_fee=overtime_fee,
                static_overtime_fee=static_overtime_fee,
                commuting_fee=commuting_fee,
            )

        salary_deduction = SalaryDeduction(
            health_insurance=health_insurance,
            nursing_insurance=nursing_insurance,
            welfare_pension=welfare_pension,
            pension_fund=pension_fund,
            employment_insurance=employment_insurance
        )

        salary_tax = SalaryTax(
            income_tax=income_tax,
            resident_tax=resident_tax,
            year_end_tax_adjustment=year_end_tax_adjustment
        )

        return Salary(
            payment_date=payment_date,
            calc_start_date=calc_start_date,
            calc_end_date=calc_end_date,
            salary_payment=salary_payment,
            salary_deduction=salary_deduction,
            salary_tax=salary_tax
        )
