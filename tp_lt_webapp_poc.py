import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="キャッシュ生産性計算ツール", layout="centered")
st.title("💰 キャッシュ生産性 (TP / LT) 計算ツール")

# データ保存用セッション
if "records" not in st.session_state:
    st.session_state.records = []

with st.form("product_form"):
    st.subheader("📥 製品データ入力")
    col1, col2 = st.columns(2)

    with col1:
        product_name = st.text_input("製品名", value="")
        purchase_date = st.date_input("材料購入日", value=date.today())
        sales = st.number_input("売上金額（円）", min_value=0, step=1000)
        
    with col2:
        shipment_date = st.date_input("出荷日", value=date.today())
        material_cost = st.number_input("材料費（円）", min_value=0, step=1000)
        outsourcing_cost = st.number_input("外注費（円）", min_value=0, step=1000)

    submitted = st.form_submit_button("追加")

    if submitted:
        lt = (shipment_date - purchase_date).days
        tp = sales - material_cost - outsourcing_cost
        tp_per_lt = tp / lt if lt > 0 else 0

        st.session_state.records.append({
            "製品名": product_name,
            "材料購入日": purchase_date,
            "出荷日": shipment_date,
            "売上": sales,
            "材料費": material_cost,
            "外注費": outsourcing_cost,
            "LT（日数)": lt,
            "TP（スループット）": tp,
            "TP/LT（キャッシュ生産性）": round(tp_per_lt, 2)
        })

# 表示
if st.session_state.records:
    st.subheader("📊 登録済データとキャッシュ生産性")
    df = pd.DataFrame(st.session_state.records)
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.subheader("📈 TP/LTの高い製品ランキング")
    st.dataframe(df.sort_values("TP/LT（キャッシュ生産性）", ascending=False).reset_index(drop=True))
