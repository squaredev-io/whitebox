import streamlit as st


def card1(text1, text2):
    st.markdown(
        f"""
    <div class="card text-white bg-dark mb-3" style="max-width: 280rem;">
        <div class="card-body">
            <p class="card-text"><b>{text1}</b></p>
            <p class="card-text">{text2}</p>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def card(text1, text2, text3):
    st.markdown(
        f"""
    <div class="card text-white bg-dark mb-3" style="width: 44rem;">
        <div class="card-body">
            <h5 class="card-title"><b>{text1}</b></h5>
            <h6 class="card-subtitle mb-2 text-muted">type: {text2}</h6>
            <p class="card-text">{text3}</p>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
