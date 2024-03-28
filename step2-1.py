import pandas as pd

######## 读取附件2中的数据 ########

# 读取企业信息、进项发票信息和销项发票信息
df_enterprise2 = pd.read_excel("question_content/附件2：302家无信贷记录企业的相关数据.xlsx", sheet_name="企业信息")
df_input_invoice2 = pd.read_excel("question_content/附件2：302家无信贷记录企业的相关数据.xlsx", sheet_name="进项发票信息")
df_output_invoice2 = pd.read_excel("question_content/附件2：302家无信贷记录企业的相关数据.xlsx", sheet_name="销项发票信息")


######## 数据处理和量化分析 ########

# 合并进项发票和销项发票信息，计算每家企业的交易额和交易差额
df_input_sum2 = df_input_invoice2.groupby("企业代号")["金额"].sum()
df_output_sum2 = df_output_invoice2.groupby("企业代号")["金额"].sum()
df_transaction2 = pd.concat([df_input_sum2, df_output_sum2], axis=1)
df_transaction2.columns = ["进项总额", "销项总额"]
df_transaction2["交易差额"] = df_transaction2["销项总额"] - df_transaction2["进项总额"]

# 合并企业信息和交易信息
df_enterprise2 = pd.merge(df_enterprise2, df_transaction2, left_on="企业代号", right_index=True)

# 根据企业的交易差额等信息，进行信贷风险量化分析
df_enterprise2["信贷风险等级"] = pd.cut(df_enterprise2["交易差额"], bins=3, labels=["高", "中", "低"])

# 根据信贷总额固定时，确定每家企业的贷款额度
total_loan_amount2 = 100000000  # 信贷总额固定为1亿元
df_enterprise2["贷款额度"] = total_loan_amount2 * df_enterprise2["交易差额"] / df_enterprise2["交易差额"].sum()


######## 制定信贷策略 ########

# 根据信贷风险等级制定贷款利率和贷款期限
df_enterprise2["贷款利率"] = df_enterprise2.apply(lambda row: 0.04 if row["信贷风险等级"] == "低" else 0.06, axis=1)
df_enterprise2["贷款期限"] = df_enterprise2.apply(lambda row: 1 if row["信贷风险等级"] == "低" else 0.5, axis=1)


######## 输出结果 ########

# 打印结果
print(df_enterprise2[["企业代号", "信贷风险等级", "贷款额度", "贷款利率", "贷款期限"]])

# 将结果保存到 Excel 文件中
df_enterprise2[["企业代号", "信贷风险等级", "贷款额度", "贷款利率", "贷款期限"]].to_excel("output_src/step2_result.xlsx", index=False)
