import streamlit as st
import plotly.express as px
import plotly.io as pio
from pyargent import Salary


def _input_salary():

    # 支給日
    payment_date: str = st.date_input("payment_date")  # field(default_factory=str, metadata={"jp": "支給日"})
    # 計算開始日
    calc_start_date: str = st.date_input("calc_start_date")  # field(default_factory=str, metadata={"jp": "計算開始日"})
    # 計算締め日
    calc_end_date: str = st.date_input("calc_end_date")  # field(default_factory=str, metadata={"jp": "計算締め日"})

    # 基本給
    basic_payment: int = st.number_input("basic_payment", min_value=0)
    # 残業代
    overtime_fee: int = st.number_input("overtime_fee", min_value=0, step=1)
    # 固定残業代
    static_overtime_fee: int = st.number_input("static_overtime_fee", min_value=0, step=1)
    # 通勤（非課税）
    commuting_fee: int = st.number_input("commuting_fee", min_value=0, step=1)

    money = st.number_input("basic_salary", min_value=0, step=1)
    text_input = st.text_input("hello")
    st.write(f"input: {text_input}, {money}")

    salary_info = Salary.from_dict({
        "payemnt_date": payment_date,
        "calc_start_date": calc_start_date,
        "calc_end_date": calc_end_date,
        "basic_payment": basic_payment,
        "overtime_fee": overtime_fee,
        "static_overtime_fee": static_overtime_fee,
        "commuting_fee": commuting_fee
    })

    if st.button("decide"):
        st.write(salary_info)
    else:
        st.write("not yet")


def main():
    # data
    data = px.data.iris()

    # side menu
    st.sidebar.markdown(
        "menu"
    )
    template = st.sidebar.selectbox(
        "Template", list(["salary_input", "other"])
    )

    if template == "salary_input":
        _input_salary()
    else:
        # body
        st.write(
            px.scatter(data, x="sepal_width", y="sepal_length")
        )


if __name__ == "__main__":
    main()
