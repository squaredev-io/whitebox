import streamlit as st


def card(paraphrased_text):
    st.markdown(
        f"""
    <div class="card text-white bg-dark mb-3" style="max-width: 280rem;">
        <div class="card-body">
            <p class="card-text">{paraphrased_text}</p>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
