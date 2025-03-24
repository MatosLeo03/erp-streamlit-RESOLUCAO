import streamlit as st
import pandas as pd
import sqlite3

def main():
    st.title("ERP Financeiro com Streamlit")

    menu = ["Clientes", "Contas a Pagar", "Contas a Receber", "Lançamentos", "Relatórios"]
    choice = st.sidebar.selectbox("Selecione uma opção", menu)

    conn = sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)

    if choice == "Clientes":
        st.subheader("Cadastro de Clientes")
        df = pd.read_sql_query("SELECT * FROM clientes", conn)
        st.dataframe(df)

    elif choice == "Contas a Pagar":
        st.subheader("Contas a Pagar")
        df = pd.read_sql_query("SELECT * FROM contas_pagar", conn)
        st.dataframe(df)

    elif choice == "Contas a Receber":
        st.subheader("Contas a Receber")
        df = pd.read_sql_query("SELECT * FROM contas_receber", conn)
        st.dataframe(df)

    elif choice == "Lançamentos":
        st.subheader("Lançamentos Financeiros")
        df = pd.read_sql_query("SELECT * FROM lancamentos", conn)
        st.dataframe(df)

    elif choice == "Relatórios":
        st.subheader("Fluxo de Caixa por Mês")
        df = pd.read_sql_query("SELECT * FROM lancamentos", conn)
        df['data_pagamento'] = pd.to_datetime(df['data_pagamento'])
        df['mes_ano'] = df['data_pagamento'].dt.to_period('M').astype(str)
        fluxo = df.groupby(['mes_ano', 'tipo'])['valor'].sum().unstack().fillna(0)
        st.bar_chart(fluxo)

        st.subheader("Status das Contas a Pagar e Receber")
        contas_pagar = pd.read_sql_query("SELECT * FROM contas_pagar", conn)
        contas_pagar['tipo'] = 'Despesa'
        contas_receber = pd.read_sql_query("SELECT * FROM contas_receber", conn)
        contas_receber['tipo'] = 'Receita'
        contas = pd.concat([contas_pagar, contas_receber])
        status = contas.groupby(['tipo', 'status'])['valor'].sum().unstack().fillna(0)
        st.bar_chart(status)

        st.subheader("Top 5 Clientes com Maior Receita")
        recebidas = contas_receber[contas_receber['status'] == 'Recebido']
        top_clientes = recebidas.groupby('cliente')['valor'].sum().nlargest(5)
        st.dataframe(top_clientes.reset_index().rename(columns={'valor': 'Receita Total'}))
        st.bar_chart(top_clientes)

    conn.close()

if __name__ == "__main__":
    main()
