import pandas as pd

# 读取之前计算得到的企业信贷风险等级和贷款额度数据
df_enterprise = pd.read_excel("output_src/step2-1_result.xlsx")

# 读取银行贷款年利率与客户流失率关系的统计数据
df_loan_loss_rate = pd.read_excel("question_content/附件3：银行贷款年利率与客户流失率关系的统计数据.xlsx")

# 定义信贷总额为1亿元
total_loan_amount = 100000000

# 根据信贷风险等级和可能的突发因素对企业的影响，调整贷款利率
df_enterprise["贷款利率"] = df_enterprise.apply(lambda row: 0.04 if row["信贷风险等级"] == "低" else 0.06, axis=1)

# 合并企业数据和贷款利率-客户流失率关系数据
df_enterprise = pd.merge(df_enterprise, df_loan_loss_rate, on="贷款利率", how="left")

# 根据贷款年利率和客户流失率关系的统计数据，预测客户流失率
# 这里可以根据实际情况使用数据进行插值或拟合，得到对应的客户流失率

# 根据客户流失率，调整贷款额度
df_enterprise["贷款额度"] *= (1 - df_enterprise["客户流失率"])

# 输出结果
print(df_enterprise[["企业代号", "信贷风险等级", "贷款额度", "贷款利率", "客户流失率"]])
# 将输出结果保存到新的 Excel 文件中
df_enterprise[["企业代号", "信贷风险等级", "贷款额度", "贷款利率", "客户流失率"]].to_excel("output_src/step3-2_result.xlsx", index=False)
