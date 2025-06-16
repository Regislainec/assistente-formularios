import streamlit as st
import zipfile, io
from datetime import date

st.set_page_config(page_title="Formulário RDP/RMP", layout="centered")
st.title("Assistente Automático - SQI004A")

# Coleta de dados
cliente = st.text_input("Cliente")
codigo_rdp = st.text_input("Código RDP")
motivos = st.multiselect("Motivos", ["Redução de Custo", "Solicitação Cliente", "Padronização", "Melhoria Técnica"])
observacoes = st.text_area("Observações")
data_inicio = st.date_input("Data de Início", value=date.today())

# Geração do conteúdo simulado
if st.button("Gerar Formulário"):
    conteudo = f"""
    Cliente: {cliente}
    Código RDP: {codigo_rdp}
    Data Início: {data_inicio}
    Motivos: {', '.join(motivos)}
    Observações: {observacoes}
    """
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        zf.writestr("formulario_SQI004A.txt", conteudo)
    st.download_button("📥 Baixar Formulário (ZIP)", buffer.getvalue(), "formulario_gerado.zip", "application/zip")
