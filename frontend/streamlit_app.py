import streamlit as st
import requests

st.set_page_config(page_title="Assistant Produit", page_icon="📊")
st.title("🤖 Assistant Produit")

st.markdown("Posez votre question sur les produits (CA, marge, fournisseur, etc.)")

question = st.text_area("Votre question", height=100)

if st.button("Envoyer la question"):
    if not question.strip():
        st.warning("Veuillez écrire une question.")
    else:
        with st.spinner("Réflexion en cours..."):
            try:
                response = requests.post(
                    "http://localhost:5000/ask",
                    json={"question": question}
                )
                if response.status_code == 200:
                    st.success("Réponse :")
                    st.write(response.json()["answer"])
                else:
                    st.error(f"Erreur serveur : {response.status_code}")
            except Exception as e:
                st.error(f"Erreur lors de la requête : {str(e)}")
