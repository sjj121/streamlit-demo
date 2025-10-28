from dataclasses import dataclass
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from io import BytesIO
from typing import Dict, List
import random
import pandas as pd
import streamlit as st


# from base_info.social_insurance import CITY_INSURANCE_CONFIGS, CITY_MIN_WAGE
@dataclass
class InsuranceItem:
    """保险项目配置"""

    name: str  # 参保项目名称
    base_min: float  # 缴纳基数下限（元）
    base_max: float  # 缴纳基数上限（元）
    company_rate: float  # 企业缴纳比例（%）
    personal_rate: float  # 个人缴纳比例（%）
    is_mandatory: bool = True  # 是否为强制参保项目
    description: str = ""  # 项目描述（可选）


# 按城市组织的保险配置
CITY_INSURANCE_CONFIGS: Dict[str, List[InsuranceItem]] = {
    '杭州': [
        InsuranceItem(
            name="养老保险",
            base_min=4812,
            base_max=24930,
            company_rate=0.16,
            personal_rate=0.08,
            is_mandatory=True,
            description="基本养老保险",
        ),
        InsuranceItem(
            name="医疗保险",
            base_min=4812,
            base_max=24930,
            company_rate=0.09,
            personal_rate=0.02,
            is_mandatory=True,
            description="基本医疗保险",
        ),
        InsuranceItem(
            name="失业保险",
            base_min=4812,
            base_max=24930,
            company_rate=0.005,
            personal_rate=0.005,
            is_mandatory=True,
            description="失业保险",
        ),
        InsuranceItem(
            name="工伤保险",
            base_min=4812,
            base_max=24930,
            company_rate=0.002,
            personal_rate=0.0,
            is_mandatory=True,
            description="工伤保险",
        ),
        InsuranceItem(
            name="生育保险",
            base_min=4812,
            base_max=24930,
            company_rate=0.0,
            personal_rate=0.0,
            is_mandatory=True,
            description="生育保险",
        ),
        InsuranceItem(
            name="住房公积金",
            base_min=2490,
            base_max=33998,
            company_rate=0.08,
            personal_rate=0.08,
            is_mandatory=True,
            description="住房公积金",
        ),
    ],
    '嘉兴': [
        InsuranceItem(
            name="养老保险",
            base_min=4812,
            base_max=24930,
            company_rate=0.16,
            personal_rate=0.08,
            is_mandatory=True,
            description="基本养老保险",
        ),
        InsuranceItem(
            name="医疗保险",
            base_min=4812,
            base_max=24930,
            company_rate=0.09,
            personal_rate=0.02,
            is_mandatory=True,
            description="基本医疗保险",
        ),
        InsuranceItem(
            name="失业保险",
            base_min=4812,
            base_max=24930,
            company_rate=0.005,
            personal_rate=0.005,
            is_mandatory=True,
            description="失业保险",
        ),
        InsuranceItem(
            name="工伤保险",
            base_min=4812,
            base_max=24930,
            company_rate=0.002,
            personal_rate=0.0,
            is_mandatory=True,
            description="工伤保险",
        ),
        InsuranceItem(
            name="生育保险",
            base_min=4812,
            base_max=24930,
            company_rate=0.0,
            personal_rate=0.0,
            is_mandatory=True,
            description="生育保险",
        ),
        InsuranceItem(
            name="住房公积金",
            base_min=2260,
            base_max=33998,
            company_rate=0.08,
            personal_rate=0.08,
            is_mandatory=True,
            description="住房公积金",
        ),
    ],
}
# 全局城市最低工资配置（单位：元/月）
CITY_MIN_WAGE = {
    '嘉兴': 2260.0,
    "杭州": 2490.0,
}


def generate_random_chinese_name():
    # 常见的中文姓氏
    surnames = [
        '张',
        '李',
        '王',
        '刘',
        '陈',
        '杨',
        '赵',
        '黄',
        '周',
        '吴',
        '徐',
        '孙',
        '胡',
        '朱',
        '高',
        '林',
        '何',
        '郭',
        '马',
        '罗',
    ]

    # 常见的中文名字用字
    given_names = [
        '伟',
        '芳',
        '娜',
        '敏',
        '静',
        '丽',
        '强',
        '磊',
        '军',
        '洋',
        '勇',
        '艳',
        '杰',
        '娟',
        '涛',
        '明',
        '超',
        '秀',
        '霞',
        '平',
        '刚',
        '桂',
        '英',
        '华',
        '亮',
        '红',
        '玲',
        '峰',
        '丽',
        '丹',
    ]

    surname = random.choice(surnames)
    # 随机生成1-2个字的名字
    name_length = random.choice([1, 2])
    given_name = ''.join(random.choices(given_names, k=name_length))

    return f"{surname}{given_name}"


def generate_sample_data():
    data = []
    for i in range(30):
        code = f"GH{i + 1:03d}"
        name = generate_random_chinese_name()
        salary = random.randint(5000, 15000)
        attendance = random.randint(0, 500)
        late = random.randint(0, 200)
        data.append(
            {
                "员工工号": code,
                "员工姓名": name,
                "税前薪资总额": salary,
                "考勤扣款": attendance,
                "迟到扣款": late,
            }
        )
    return data


def get_template_excel():
    output = BytesIO()
    # template_data = {
    #     "员工工号": ["GH001", "GH002"],
    #     "员工姓名": ["张三", "李四"],
    #     "税前薪资总额": [15000.0, 12000.0],
    #     "考勤扣款": [0.0, 300.0],
    #     "迟到扣款": [0.0, 100.0],
    #     # "社保补贴": [300.0, 400.0],
    #     # "年休假预发补贴": [500.0, 0.0],
    #     # "职务补贴": [0.0, 1000.0],
    #     # "技能补贴": [0.0, 500.0],
    #     # "合同到期补贴": [100.0, 200.0],
    # }
    template_data = generate_sample_data()
    df = pd.DataFrame(template_data)

    with pd.ExcelWriter(output, engine='openpyxl') as writer:  # noqa
        df.to_excel(writer, index=False, sheet_name="员工薪资数据")
    output.seek(0)
    return output


def calculate_insurance_details(city_key, total_target_salary):
    # 五险一金计算
    details = []
    insurance_items = CITY_INSURANCE_CONFIGS.get(city_key, [])
    company_basic_total = 0.0  # 按最低基数
    company_full_total = 0.0  # 足额缴纳
    personal_basic_total = 0.0  # 按最低基数
    personal_housing_fund = 0.0  # 单独记录公积金个人部分（数值）

    for insurance_item in insurance_items:
        base = insurance_item.base_min
        company_basic_pay = float(
            Decimal(str(base * insurance_item.company_rate)).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
        )
        personal_basic_pay = float(
            Decimal(str(base * insurance_item.personal_rate)).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
        )
        company_full_pay = float(
            Decimal(str(total_target_salary * insurance_item.company_rate)).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
        )

        if "住房公积金" in insurance_item.name:
            company_basic_pay = float(
                Decimal(str(company_basic_pay)).quantize(
                    Decimal('1'), rounding=ROUND_HALF_UP
                )
            )
            company_full_pay = float(
                Decimal(str(company_full_pay)).quantize(
                    Decimal('1'), rounding=ROUND_HALF_UP
                )
            )
            personal_basic_pay = float(
                Decimal(str(personal_basic_pay)).quantize(
                    Decimal('1'), rounding=ROUND_HALF_UP
                )
            )
            personal_housing_fund = personal_basic_pay  # 保存原始数值

        personal_basic_total += personal_basic_pay
        company_basic_total += company_basic_pay
        company_full_total += company_full_pay

        details.append(
            {
                "保险项目": insurance_item.name,
                "缴费基数": f"{base:,.0f}",
                "企业比例": f"{insurance_item.company_rate * 100:.2f}%",
                "企业缴纳": f"¥{company_basic_pay:,.2f}",
                "个人比例": f"{insurance_item.personal_rate * 100:.2f}%",
                "个人缴纳": f"¥{personal_basic_pay:,.2f}",
                # 👇 保留原始数值，用于后续计算
                # "_personal_amount": personal_basic_pay,
                # "_company_amount": company_basic_pay,
            }
        )
    return (
        details,
        company_basic_total,
        company_full_total,
        personal_basic_total,
        personal_housing_fund,
    )


def calculate_tax(income):
    levels = [
        (3000, 0.03, 0),
        (12000, 0.10, 210),
        (25000, 0.20, 1410),
        (35000, 0.25, 2660),
        (55000, 0.30, 4410),
        (80000, 0.35, 7160),
        (float('inf'), 0.45, 15160),
    ]

    income_decimal = Decimal(str(income))

    for limit, rate, quick_deduction in levels:
        if income <= limit:
            rate_decimal = Decimal(str(rate))
            quick_deduction_decimal = Decimal(str(quick_deduction))
            limit_decimal = Decimal(str(limit))

            if income_decimal <= limit_decimal:
                result = income_decimal * rate_decimal - quick_deduction_decimal
                # 四舍五入到分（两位小数）
                return float(result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

    result = income_decimal * Decimal('0.45') - Decimal('15160')
    return float(result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))


st.set_page_config(page_title="薪安管理系统", page_icon="💰", layout='wide')
st.header("🧮 薪资核算")

st.markdown("### 基本信息")

col_city, col_month, col_range, col_pnum, col_status, col_tmp = st.columns(6)
with col_city:
    city_key = st.selectbox(
        label='选择城市', options=list(CITY_INSURANCE_CONFIGS.keys()), index=1
    )
with col_month:
    st.selectbox(
        label='核算月份',
        options=[i for i in range(1, 13)],
        index=datetime.now().month - 1,
    )
with col_range:
    st.selectbox(label='核算范围', options=[], placeholder="请选择")
with col_pnum:
    st.selectbox(label="核算人数", options=[], placeholder="自动计算", disabled=True)
with col_status:
    st.selectbox(label='状态', options=[], placeholder="新建")
with col_tmp:
    st.selectbox(label='薪资模板', options=[], placeholder="请选择")


# st.markdown("### 📥 上传员工数据 Excel 文件")
st.markdown('---')
template_file = get_template_excel()
st.download_button(
    label="📥 下载 Excel 导入模板",
    data=template_file,
    file_name="薪资输入模板.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    width='stretch',
)

st.markdown("### Excel导入核算")
uploaded_file = st.file_uploader(
    "通过Excel模板导入进行核算", type=['xlsx'], width='stretch'
)
st.markdown("### 📊 批量核算结果")
if uploaded_file:
    try:
        df_input = pd.read_excel(uploaded_file)
        # city_key = '嘉兴'
        results = []
        for index, item in df_input.iterrows():
            staff_code = item['员工工号']
            staff_name = item['员工姓名']
            target_total_salary = item['税前薪资总额']

            # 基本工资
            basic_salary = CITY_MIN_WAGE.get(city_key, 3000)

            # 计算五险一金
            (
                details,
                company_basic_total,
                company_full_total,
                personal_basic_total,
                personal_housing_fund,
            ) = calculate_insurance_details(city_key, target_total_salary)

            # 社保补贴
            social_insurance_allowance = (
                float(item.get('社保补贴', 0) or 0)
                or company_full_total - company_basic_total
            )

            # 考勤扣款
            attendance_deduction = float(item.get('考勤扣款', 0.0))
            # 迟到扣款
            lateness_deduction = float(item.get('迟到扣款', 0.0))

            # 年休假预发补贴
            annual_leave_prepay_amount = float(item.get('年休假预发补贴', 500.0))
            # 职务补贴
            position_allowance = float(item.get('职务补贴', 0.0))
            # 技能补贴
            skill_allowance = float(item.get('技能补贴', 0.0))
            # 合同到期补贴
            contract_end_allowance = float(item.get('合同到期补贴', 0.0))

            # 实际税前 扣除考勤和迟到扣款
            actual_total_salary = (
                target_total_salary - attendance_deduction - lateness_deduction
            )
            # 税前总额 应发
            gross_income = actual_total_salary
            # 实际可拆分的绩效部分
            performance_temp = actual_total_salary - basic_salary

            performance = (
                performance_temp
                - annual_leave_prepay_amount
                - position_allowance
                - skill_allowance
                - contract_end_allowance
                - social_insurance_allowance
            )

            pre_tax_deduction = personal_basic_total  # 个人五险一金（税前扣除）
            # 预估个税
            person_tax = calculate_tax(
                max(gross_income - personal_basic_total - 5000, 0)
            )
            net_salary = gross_income - pre_tax_deduction - person_tax  # 实发
            # 企业总成本
            total_company_cost = gross_income + company_basic_total

            results.append(
                {
                    "员工工号": staff_code,
                    "员工姓名": staff_name,
                    "税前薪资总额": f"{target_total_salary:.2f}",
                    "基本工资": f"{basic_salary:.2f}",
                    "绩效工资": f"{performance:.2f}",
                    "考勤扣款": f'{attendance_deduction:.2f}',
                    "迟到扣款": f'{lateness_deduction:.2f}',
                    "职务补贴": f"{position_allowance:.2f}",
                    "技能补贴": f"{skill_allowance:.2f}",
                    "社保补贴": f"{social_insurance_allowance:.2f}",
                    "年休假预发补贴": f"{annual_leave_prepay_amount:.2f}",
                    "合同到期补贴": f"{contract_end_allowance:.2f}",
                    "应发工资": f"{gross_income:.2f}",
                    "社保个人缴纳": f"{personal_basic_total - personal_housing_fund:.2f}",
                    "公积金个人缴纳": f"{personal_housing_fund:.2f}",
                    "预估个人所得税": f"{person_tax:.2f}",
                    "预估实发": f"{net_salary:.2f}",
                    "企业社保公积金": f"{company_basic_total:.2f}",
                    "企业总成本": f"{total_company_cost:.2f}",
                }
            )
        results_df = pd.DataFrame(results)

        st.dataframe(results_df, hide_index=True, width='stretch')

        # === 导出功能 ===
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:  # noqa
            results_df.to_excel(writer, index=False, sheet_name='薪资拆分')
        output.seek(0)
        st.download_button(
            label="📥 下载结果 Excel",
            data=output,
            file_name=f'薪资核算结果_{datetime.now().strftime('%y%m')}.xlsx',
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width='stretch',
        )

    except Exception as e:
        st.toast(str(e))
