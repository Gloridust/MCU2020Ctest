import pandas as pd

# 读取银行贷款年利率与客户流失率关系的统计数据
df_loss_rate = pd.read_excel("question_content/附件3：银行贷款年利率与客户流失率关系的统计数据.xlsx")

# 定义根据信贷风险等级和突发因素制定信贷调整策略的函数
def adjust_credit_strategy(credit_risk, impact_factor):
    # 根据信贷风险等级和突发因素综合评估，制定信贷调整策略

    if credit_risk == "高":
        if impact_factor == "严重影响":
            return "贷款利率提高，贷款期限缩短"
        elif impact_factor == "一般影响":
            return "贷款利率略微提高，贷款期限略微缩短"
    elif credit_risk == "中":
        if impact_factor == "严重影响":
            return "贷款利率略微提高"
        elif impact_factor == "一般影响":
            return "贷款利率不变"
    elif credit_risk == "低":
        return "贷款利率不变，可适当放宽贷款条件"

# 对每个企业综合考虑信贷风险和突发因素，制定信贷调整策略
df_enterprise["信贷调整策略"] = df_enterprise.apply(lambda row: adjust_credit_strategy(row["信贷风险等级"], row["突发因素"]), axis=1)

# 输出结果
print(df_enterprise[["企业代号", "信贷风险等级", "突发因素", "信贷调整策略"]])
# 将输出结果保存到新的 Excel 文件中
df_enterprise[["企业代号", "信贷风险等级", "突发因素", "信贷调整策略"]].to_excel("output_src/step3-1_result.xlsx", index=False)
