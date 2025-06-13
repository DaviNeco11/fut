import streamlit as st
import json
from datetime import datetime

# Carrega os dados do JSON (cole aqui o JSON ou use um arquivo externo)
with open("outputs/report.json", "r", encoding="utf-8") as file:
    data = json.load(file)

st.set_page_config(page_title="Relatório de Validação FHIR", layout="wide")

# Título principal
st.title("📋 Relatório de Validação FHIR")

# Resumo geral
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Testes", data["total_tests"])
col2.metric("✅ Passaram", data["passed"])
col3.metric("❌ Falharam", data["failed"])
col4.metric("⏱ Tempo Total", f'{data["total_time_sec"]:.2f} s')

# Exibir execução por teste
st.header("Detalhes dos Testes")

for test in data["tests"]:
    with st.expander(f'🧪 Teste: `{test["test_id"]}` - {"✅ Passou" if test["status"] == "passed" else "❌ Falhou"}'):
        st.markdown(f"**Status:** `{test['status']}`")
        st.markdown(f"**Tempo de execução:** `{test['exec_time_sec']:.2f} s`")

        if test["input_instance"]:
            st.subheader("🔸 Entrada (JSON)")
            st.json(json.loads(test["input_instance"]))

        if test["expected_results"]:
            st.subheader("📌 Resultados Esperados")
            for r in test["expected_results"]:
                st.write(f"- `{r['severity']}`: {r['diagnostics']} ({r['location']})")

        if test["obtained_results"]:
            st.subheader("📌 Resultados Obtidos")
            for r in test["obtained_results"]:
                st.write(f"- `{r['severity']}`: {r['diagnostics']} ({r['location']})")

        if test["differences"]:
            st.subheader("⚠️ Diferenças ou Erros")
            for diff in test["differences"]:
                st.error(diff)

        if test["raw_validator_output"]:
            st.subheader("📄 Saída Bruta do Validador (log)")
            st.text_area("Raw Output", test["raw_validator_output"], height=300)
