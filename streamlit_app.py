import streamlit as st
from zipfile import ZipFile
from datetime import date
from odf.opendocument import load
from odf.text import P, Span

# Função para preencher campos no .odt
def preencher_odt(campos, modelo_path, saida_path):
    doc = load(modelo_path)

    for p in doc.getElementsByType(P):
        # Captura apenas o texto contido nos nós de texto simples
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
            # Remove todos os elementos filhos do parágrafo
            for node in list(p.childNodes):
                p.removeChild(node)
            # Adiciona um novo conteúdo com o texto substituído
            span = Span(text=full_text)
            p.addElement(span)

    doc.save(saida_path)

# Configuração da página
st.set_page_config(page_title="Formulário SQI004A", layout="centered")
st.title("Assistente Automático - SQI004A")

# Formulário de entrada de dados
cliente = st.text_input("Cliente")
preco_mercado = st.text_input("Preço Mercado (R$)")
contato = st.text_input("Contato")
potencial = st.text_input("Potencial de Mercado (pcs/ano)")
cod_produto_cliente = st.text_input("Código do Produto do Cliente")
produto_intelli = st.text_input("Nome Inicial do Produto Intelli")
especificacoes = st.text_area("Desenho / Especificações")
normas = st.text_input("Normas")
motivos = st.text_area("Motivos")
processos = st.text_area("Processos Envolvidos")
ferramentas = st.text_area("Ferramentas Envolvidas")
anexos = st.text_area("Anexos")
observacoes = st.text_area("Observações")
data_inicio = st.date_input("Data de Início do Processo", value=date.today())
data_conclusao = st.date_input("Data Estimada para Conclusão", value=date.today())

# Ao clicar no botão
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
        st.download_button(
            label="📥 Baixar Relatório Gerado (.zip)",
            data=f.read(),
            file_name="SQI004A_final.zip",
            mime="application/zip"
        )
