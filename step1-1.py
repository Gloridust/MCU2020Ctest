import pandas as pd

# 读取企业信息、进项发票信息和销项发票信息
df_enterprise = pd.read_excel("附件1：123家有信贷记录企业的相关数据.xlsx", sheet_name="企业信息")
df_input_invoice = pd.read_excel("附件1：123家有信贷记录企业的相关数据.xlsx", sheet_name="进项发票信息")
df_output_invoice = pd.read_excel("附件1：123家有信贷记录企业的相关数据.xlsx", sheet_name="销项发票信息")

# 合并进项发票和销项发票信息，计算每家企业的交易额
df_input_sum = df_input_invoice.groupby("企业代号")["金额"].sum()
df_output_sum = df_output_invoice.groupby("企业代号")["金额"].sum()
df_transaction = pd.concat([df_input_sum, df_output_sum], axis=1)
df_transaction.columns = ["进项总额", "销项总额"]
df_transaction["交易差额"] = df_transaction["销项总额"] - df_transaction["进项总额"]

# 合并企业信息和交易信息
df_enterprise = pd.merge(df_enterprise, df_transaction, left_on="企业代号", right_index=True)

# 根据企业的交易差额等信息，进行信贷风险量化分析（这里仅做示例，实际分析需根据具体情况确定）
df_enterprise["信贷风险等级"] = pd.cut(df_enterprise["交易差额"], bins=3, labels=["高", "中", "低"])

# 根据信贷总额固定时，确定每家企业的贷款额度（这里仅做示例，实际根据具体情况确定）
total_loan_amount = 1000000  # 信贷总额固定为100万元
df_enterprise["贷款额度"] = total_loan_amount * df_enterprise["交易差额"] / df_enterprise["交易差额"].sum()

# 输出结果
print(df_enterprise[["企业代号", "信贷风险等级", "贷款额度"]])
