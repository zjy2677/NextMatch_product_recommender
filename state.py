import streamlit as st

ORDER = ["country", "customer_id", "gender", "sport", "product_type", "subtype", "price_range"]

def init_state():
    st.session_state.setdefault("step", 0)
    st.session_state.setdefault("answers", {})
    st.session_state.setdefault("result_df", None)
    st.session_state.setdefault("client_id_verified", False)

def reset_quiz():
    st.session_state.step = 0
    st.session_state.answers = {}
    st.session_state.result_df = None
    st.session_state.client_id_verified = False

def clear_downstream_answers(changed_qid: str):
    if changed_qid not in ORDER:
        return

    i = ORDER.index(changed_qid)
    for k in ORDER[i + 1 :]:
        st.session_state.answers.pop(k, None)

    if changed_qid in ("country", "customer_id"):
        st.session_state.client_id_verified = False

    st.session_state.result_df = None
