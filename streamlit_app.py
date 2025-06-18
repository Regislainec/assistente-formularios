import streamlit as st
from zipfile import ZipFile
from datetime import date
from odf.opendocument import load
from odf.text import P

def preencher_odt(campos, modelo_path, saida_path):
    doc = load(modelo_path)
    for p in doc.getElementsByType(P):
        full_text = "".join(
            node.data for node in p.childNodes if node.nodeType == 3
        )

        atualizado = False
        for chave, valor in campos.items():
            marcador = f"{{{{{chave}}}}}"
            if marcador in full_text:
                full_text = full_text.replace(marcador, valor)
                atualizado = True

        if atualizado:
            while p.hasChildNodes():
                p.removeChild(p.firstChild)
            p.addText(full_text)

    doc.save(saida_path)

st.set_page_config(page_title="Formulário SQI004A", layout="centered")
st.title("Preenchimento Automático - SQI004A")

# Campos do formulário
cliente = st.text_input("Cliente")
preco_mercado = st.text_input("Preço Mercado")
contato = st.text_input("Contato")
potencial = st.text_input("Potencial")
cod_produto_cliente = st.text_input("Código Produto Cliente")
produto_intelli = st.text_input("Produto Intelli")
especificacoes = st.text_area("Especificações / Desenho")
normas = st.text_input("Normas")
motivos = st.text_area("Motivos")
processos = st.text_area("Processos Envolvidos")
ferramentas = st.text_area("Ferramentas Envolvidas")
anexos = st.text_area("Anexos")
observacoes = st.text_area("Observações")
data_inicio = st.date_input("Data de Início", value=date.today())
data_conclusao = st.date_input("Data de Conclusão")

if st.button("Gerar Relatório"):
    campos = {
        "cliente": cliente,
        "preco_mercado": preco_mercado,
        "contato": contato,
        "potencial": potencial,
        "cod_produto_cliente": cod_produto_cliente,
        "produto_intelli": produto_intelli,
        "especificacoes": especificacoes,
        "normas": normas,
        "motivos": motivos,
        "processos": processos,
        "ferramentas": ferramentas,
        "anexos": anexos,
        "observacoes": observacoes,
        "data_inicio": str(data_inicio),
        "data_conclusao": str(data_conclusao)
    }

    modelo = "templates/SQI004A_modelo_marcado.odt"
    saida = "SQI004A_preenchido.odt"
    preencher_odt(campos, modelo, saida)

    with ZipFile("SQI004A_final.zip", "w") as zf:
        zf.write(saida)

    with open("SQI004A_final.zip", "rb") as f:
        st.download_button("📥 Baixar Relatório (ZIP)", f.read(), "SQI004A_final.zip", "application/zip")
