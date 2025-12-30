import streamlit as st
import google.generativeai as genai

# 1. Configuração da Página
st.set_page_config(page_title="Santo Conselho", page_icon="🙏")

# 2. Configuração da API (A chave será configurada no painel do Streamlit depois)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Chave API não encontrada nas configurações.")

st.title("🙏 Santo Conselho")
st.write("Orientação espiritual fiel ao Magistério da Igreja.")

# 3. Interface de Usuário
pergunta = st.text_area("Compartilhe sua dúvida ou situação:",
                        placeholder="Ex: Como posso me preparar melhor para ser Ministro da Eucaristia?")

if st.button("Buscar Conselho"):
    if pergunta:
        # O Spinner mantém o usuário calmo enquanto o 27B processa
        with st.spinner("Consultando a sabedoria dos santos..."):
            try:
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