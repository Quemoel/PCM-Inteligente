#
import streamlit as st
import math
import pandas as pd

# Configuração da página
st.set_page_config(page_title="PCM Inteligente", layout="centered", page_icon="📈")

# Estilo CSS customizado
st.markdown("""
    <style>
        /* Fundo da página */
        .stApp {
            background: linear-gradient(135deg, #00509E, #00A896);
            padding: 20px;
        }

        

        /* Título principal */
        .titulo {
            font-size: 42px;
            color: #FFFFFF;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
            text-transform: uppercase;
        }

        /* Subtítulos */
        .subtitulo {
            font-size: 20px;
            color: #000000;
            text-align: center;
            margin-bottom: 25px;
            font-style: italic;
        }

        /* Inputs e seletores estilizados */
        .stSelectbox, .stTextInput, .stNumberInput {
            background-color: #FFFFFF;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 15px;
            border: 2px solid #00509E;
            transition: all 0.3s ease;
        }

        .stSelectbox:hover, .stTextInput:hover, .stNumberInput:hover {
            border-color: #00A896;
            transform: scale(1.02);
        }

        /* Expansores */
        .stExpander {
            border: 2px solid #00509E;
            border-radius: 12px;
            padding: 15px;
            background-color: #EAF2FF;
            transition: all 0.3s ease;
        }

        .stExpander:hover {
            border-color: #00A896;
            background-color: #DFFFF6;
        }

        /* Caixa de resultado */
        .resultado {
            background-color: #FFFFFF;
            border-left: 6px solid #00509E;
            padding: 20px;
            margin-top: 20px;
            border-radius: 12px;
            box-shadow: 2px 2px 15px rgba(0, 0, 0, 0.15);
            font-size: 18px;
            color: #222;
            font-weight: bold;
        }

        /* Botão principal */
        div.stButton > button {
            background-color: #00A896;
            color: #FFFFFF;
            font-size: 16px;
            font-weight: bold;
            border: none;
            padding: 12px 25px;
            border-radius: 10px;
            transition: 0.3s;
            cursor: pointer;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        }

        div.stButton > button:hover {
            background-color: #00509E;
            transform: scale(1.05);
            box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.3);
        }
    </style>
""", unsafe_allow_html=True)

# Container principal estilizado
st.markdown("<div class='main-container'>", unsafe_allow_html=True)

# Cabeçalho com título e subtítulo
st.markdown("<div class='titulo'>PCM Inteligente</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitulo'>Cálculos Inteligentes para Planejamento de Manutenção</div>", unsafe_allow_html=True)

# Seletor de análises
opcao = st.selectbox("Selecione uma análise:", [
    "CPMR - Custo de Manutenção x Reposição",
    "Apropriação de Horas por Tipo de Manutenção",
    "Confiabilidade Projetada",
    "MTBF e Frequência Ideal",
    "MTTR - Tempo Médio para Reparos"
])

st.markdown("</div>", unsafe_allow_html=True)




#teste






# 1. CPMR
if opcao == "CPMR - Custo de Manutenção x Reposição":
    st.subheader("CPMR - Custo de Manutenção x Reposição")
    manutencao = st.number_input("Gasto anual com manutenção (R$)", min_value=0.0)
    reposicao = st.number_input("Valor de reposição do equipamento (R$)", min_value=0.0)

    if st.button("Calcular CPMR"):
        cpmm = (manutencao / reposicao) * 100
        limite = 2.5
        if cpmm > limite:
            recomendacao = f"<b>CPMR = {cpmm:.2f}%</b> - Acima do limite. <span style='color:red;'>Recomendado substituir o equipamento.</span>"
        else:
            recomendacao = f"<b>CPMR = {cpmm:.2f}%</b> - Abaixo do limite. <span style='color:green;'>Recomendado manter o equipamento.</span>"
        st.markdown(f"<div class='resultado'>{recomendacao}</div>", unsafe_allow_html=True)

# 2. Apropriação de Horas
elif opcao == "Apropriação de Horas por Tipo de Manutenção":
    st.subheader("Apropriação de Horas por Tipo de Manutenção")
    hora_planejada = st.number_input("Hora Planejada Total", min_value=00)

    setores = ["Corretiva", "Emergencial", "Preditiva", "Preventiva", "Inspeções"]
    dados = {}

    for setor in setores:
        with st.expander(f"Setor: {setor}"):
            pessoas = st.number_input(f"{setor} - Pessoas", key=f"p_{setor}", min_value=0)
            horas_dia = st.number_input(f"{setor} - Horas", key=f"h_{setor}", min_value=00)
            dias = st.number_input(f"{setor} - Dias", key=f"d_{setor}", min_value=0)
            dados[setor] = pessoas * horas_dia * dias

    setor_base = st.selectbox("Setor base para apropriação:", setores)

    if st.button("Calcular Apropriação"):
        total_geral = sum(dados.values())
        if total_geral == 0:
            st.error("Preencha ao menos um setor com valores válidos.")
        else:
            apropr_setor = (dados[setor_base] / total_geral) * 100
            apropr_total = (total_geral / hora_planejada) * 100
            faltante = 100 - apropr_total

            resultado = f"""
                <b>Total de Horas:</b> {total_geral:.2f}h<br>
                <b>Apropriação do setor '{setor_base}':</b> {apropr_setor:.2f}%<br>
                <b>Apropriação Total:</b> {apropr_total:.2f}%<br>
                <b>Faltante para 100%:</b> {faltante:.2f}%
            """
            st.markdown(f"<div class='resultado'>{resultado}</div>", unsafe_allow_html=True)

# 3. Confiabilidade Projetada
elif opcao == "Confiabilidade Projetada":
    st.subheader("Confiabilidade Projetada")
    tempo_total = st.number_input("Tempo Operacional Total (dias)", min_value=00)
    falhas = st.number_input("Número de Falhas", min_value=0)
    tempo_prev = st.number_input("Tempo de Previsão (dias)", min_value=00)

    if st.button("Calcular Confiabilidade"):
        if falhas == 0:
            st.error("Número de falhas não pode ser zero.")
        else:
            mtbf = tempo_total / falhas
            lamb = 1 / mtbf
            confiab = math.exp(-lamb * tempo_prev) * 100
            resultado = f"""
                <b>MTBF:</b> {mtbf:.2f} dias<br>
                <b>Taxa de falha (λ):</b> {lamb:.4f}<br>
                <b>Confiabilidade Projetada:</b> {confiab:.2f}%
            """
            st.markdown(f"<div class='resultado'>{resultado}</div>", unsafe_allow_html=True)

# 4. MTBF e Frequência Ideal
elif opcao == "MTBF e Frequência Ideal":
    st.subheader("MTBF e Frequência Ideal")
    lista_horas = st.text_input("Horas de Operação Trabalhadas (ex: 500,125,500,1200,800)")
    falhas = st.number_input("Número de Falhas", min_value=0)

    if st.button("Calcular MTBF"):
        horas = [float(h.strip()) for h in lista_horas.split(",") if h.strip()]
        mtbf = sum(horas) / falhas if falhas > 0 else 0
        st.markdown(f"<div class='resultado'><b>MTBF:</b> {mtbf:.2f} horas</div>", unsafe_allow_html=True)

# 5. MTTR - Tempo Médio para Reparos (em minutos)
elif opcao == "MTTR - Tempo Médio para Reparos":
    st.subheader("MTTR - Tempo Médio para Reparos (em minutos)")

    tempo_reparo = st.text_input("Tempo de Reparo (em minutos, ex: 120,90,45)", help="Insira os tempos de reparo separados por vírgula")
    falhas_mttr = st.number_input("Número de Falhas", min_value=1, help="Número total de falhas que exigiram reparo")

    if st.button("Calcular MTTR"):
        try:
            tempos = [float(t.strip()) for t in tempo_reparo.split(",") if t.strip()]

            if len(tempos) == 0:
                st.error("Insira pelo menos um tempo de reparo válido.")
            else:
                mttr = sum(tempos) / falhas_mttr
                resultado_mttr = f"""
                    <b>MTTR:</b> {mttr:.2f} minutos<br>
                    <b>Total de Tempo de Reparo:</b> {sum(tempos):.2f} minutos<br>
                    <b>Número de Falhas:</b> {falhas_mttr}
                """
                st.markdown(f"<div class='resultado'>{resultado_mttr}</div>", unsafe_allow_html=True)
        except ValueError:
            st.error("Formato inválido. Insira os tempos de reparo separados por vírgula (ex: 120,90,45).")




#extras

