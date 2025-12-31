import streamlit as st
import google.generativeai as genai

# 1. Configuração da Página
st.set_page_config(page_title="Santo Conselho", page_icon="🙏")

# --- AJUSTE ESTÉTICO: CSS para o Botão ---
st.markdown(f"""
    <style>
    div.stButton > button {{
        background-color: #4B5563; /* A cor que você escolheu */
        color: white;
        border-radius: 5px;
        height: 3em;
        width: 100%;
        font-weight: bold;
        border: none;
    }}
    div.stButton > button:hover {{
        background-color: #374151; /* Tom levemente mais escuro para o efeito de passar o mouse */
        color: white;
    }}
    </style>
""", unsafe_allow_html=True)

# 2. Inserindo a Logo (Certifique-se de que o arquivo logo1 está no GitHub com a extensão correta)
try:
    # Ajustei para logo1.png como padrão; se for .jpg, altere abaixo
    st.image("logo1.png", width=150)
except:
    st.write("🙏 **Santo Conselho**")

# 3. Configuração da API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Chave API não encontrada nas configurações.")

st.title("Santo Conselho")
st.write("Orientação espiritual fiel ao Magistério da Igreja.")

# 4. Interface de Usuário
pergunta = st.text_area("Compartilhe sua dúvida ou situação:",
                        placeholder="Ex: Como posso me preparar melhor para ser Ministro da Eucaristia?")

if st.button("Buscar Conselho"):
    if pergunta:
        with st.spinner("Consultando a sabedoria dos santos..."):
            try:
                # Uso do modelo de alta performance Gemma 3-27B
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
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Erro ao processar: {e}")
    else:
        st.warning("Por favor, escreva sua pergunta antes de enviar.")