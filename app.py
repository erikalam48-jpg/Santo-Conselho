import streamlit as st
import google.generativeai as genai

# 1. Configuração da Página
st.set_page_config(page_title="Santo Conselho", page_icon="🙏", layout="centered")

# --- AJUSTE ESTÉTICO: Centralização e Cores ---
st.markdown(f"""
    <style>
    /* Centraliza todo o conteúdo do site */
    .main .block-container {{
        text-align: center;
    }}

    /* Muda a cor do título e centraliza */
    h1 {{
        color: #4B5563 !important;
        text-align: center;
        font-weight: bold;
    }}

    /* Centraliza o texto dentro da caixa de pergunta */
    .stTextArea textarea {{
        text-align: center;
    }}

    /* Estilo do Botão (Mantendo sua cor #4B5563) */
    div.stButton > button {{
        background-color: #4B5563;
        color: white;
        border-radius: 5px;
        height: 3em;
        width: 100%;
        font-weight: bold;
        border: none;
    }}
    div.stButton > button:hover {{
        background-color: #374151;
        color: white;
    }}
    </style>
""", unsafe_allow_html=True)

# 2. Inserindo a Logo Centralizada (Ajuste de Proporção para diminuir o tamanho)
# Aumentamos as laterais (2.5) e diminuímos o meio (1) para a logo ficar menor
col1, col2, col3 = st.columns([2.5, 1, 2.5])
with col2:
    try:
        # use_container_width=True agora preenche apenas esse espaço menor central
        st.image("logo1.png", use_container_width=True)
    except:
        st.write("🙏")

# 3. Configuração da API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Chave API não encontrada nas configurações.")

# Título e Subtítulo centralizados
st.title("Santo Conselho")
st.write("Orientação espiritual fiel ao Magistério da Igreja.")

# 4. Interface de Usuário
pergunta = st.text_area("Compartilhe sua dúvida ou situação:",
                        placeholder="Ex: Como posso me preparar melhor para ser Ministro da Eucaristia?")

if st.button("Buscar Conselho"):
    if pergunta:
        with st.spinner("Consultando a sabedoria dos santos..."):
            try:
                # Sua lógica original do Gemma 3-27B
                model = genai.GenerativeModel(
                    model_name='models/gemma-3-27b-it',
                    generation_config={"max_output_tokens": 800, "temperature": 0.7}
                )

                instrucao = (
                    "Persona: Santo Conselho, sábio católico fiel ao Magistério e ao catecismo. "
                    "Missão: Conselhos breves com caridade e verdade. Cite santos. Mantenha a precisão doutrinária, mas com um toque humano e variado. "
                    "Regra: Seja rigoroso com fatos bíblicos, Nunca contradiga dogmas. Sempre varie as metáforas, saudações, conclusões, exemplos de santos e passagens bíblicas. "
                    "Casos graves (saúde/mental): oriente padre e médico. "
                )

                response = model.generate_content(f"{instrucao}\nPergunta: {pergunta}")
                st.markdown("---")
                # O texto da resposta também aparecerá centralizado
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Erro ao processar: {e}")
    else:
        st.warning("Por favor, escreva sua pergunta antes de enviar.")