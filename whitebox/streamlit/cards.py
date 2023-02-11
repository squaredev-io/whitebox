import streamlit as st


def card(text):
    st.markdown(
        f"""
    <div class="card text-white bg-dark mb-3" style="max-width: 280rem;">
        <div class="card-body">
            <p class="card-text">{text}</p>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
