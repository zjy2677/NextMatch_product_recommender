from pathlib import Path

import pandas as pd
import streamlit as st

from config import COUNTRIES, DEBUG_MODE
from data_loader import get_stock_df, get_catalog_df_for_country
from questions import QUESTIONS
from sql import query_stock
from state import init_state, reset_quiz, clear_downstream_answers
from taxonomy import TAXONOMY
from ui.demo_images import DEMO_PRODUCT_IMAGES
'''
This module contains the main logic to render the Streamlit app, including:
- Rendering questions and input widgets based on the QUESTIONS definition.
- Handling user navigation (Next/Back buttons).
- Displaying results and personalized recommendations if customer ID is provided and verified.
- Verifying customer ID against the catalog for the selected country.'''

def verify_customer_id(country: str, customer_id_raw: str) -> tuple[bool, str]:
    customer_id = (customer_id_raw or "").strip()
    if customer_id == "":
        return True, ""

    try:
        catalog_df = get_catalog_df_for_country(country)
    except Exception as e:
        return False, f"Failed to load catalog for {country}: {e}"

    if "ClientID" not in catalog_df.columns:
        return False, 'Catalog file is missing required column "ClientID".'

    series = catalog_df["ClientID"].astype(str).str.strip()
    if (series == customer_id).any():
        return True, "Client ID found ✅"

    return False, "Client ID not found, please double check your ID, your country and region"


def show_results_with_optional_images(df: pd.DataFrame, title: str):
    st.success(title)

    if df is None or df.empty:
        st.info("No products found.")
        return

    for _, r in df.iterrows():
        product = str(r.get("product", "")).strip()
        status = str(r.get("status", "")).strip()
        price = r.get("price", None)

        img_path = DEMO_PRODUCT_IMAGES.get(product)
        price_text = None
        if pd.notna(price):
            try:
                price_text = f"€{float(price):.2f}"
            except Exception:
                price_text = None

        if img_path and Path(img_path).exists():
            c1, c2 = st.columns([1, 3], vertical_alignment="center")
            with c1:
                st.image(str(img_path), use_container_width=True)
            with c2:
                st.markdown(f"**{product}**")
                if price_text:
                    st.caption(f"Price: {price_text}")
                if status:
                    st.caption(f"Status: {status}")
        else:
            st.markdown(f"**{product}**")
            if price_text:
                st.caption(f"Price: {price_text}")
            if status:
                st.caption(f"Status: {status}")

        st.divider()


def render_question(step: int):
    q = QUESTIONS[step]
    qid = q["id"]
    widget = q["widget"]

    st.markdown(f"<div class='big-question'>{q['text']}</div>", unsafe_allow_html=True)

    if qid == "product_type":
        sport = st.session_state.answers.get("sport")
        if not sport:
            st.warning("Please choose a sport first.")
            st.stop()
        q["options"] = list(TAXONOMY[sport].keys())

    if qid == "subtype":
        sport = st.session_state.answers.get("sport")
        ptype = st.session_state.answers.get("product_type")
        if not sport or not ptype:
            st.warning("Please choose sport and product type first.")
            st.stop()
        q["options"] = TAXONOMY[sport][ptype]

    if widget == "text_input":
        prev = st.session_state.answers.get(qid, "")
        return st.text_input(
            label=" ",
            value=prev,
            key=f"w_{qid}",
            label_visibility="collapsed",
        )

    options = q["options"]
    prev = st.session_state.answers.get(qid, options[0] if options else None)

    if widget == "selectbox":
        idx = options.index(prev) if prev in options else 0
        return st.selectbox(
            label=" ",
            options=options,
            index=idx,
            key=f"w_{qid}",
            label_visibility="collapsed",
        )

    idx = options.index(prev) if prev in options else 0
    return st.radio(
        label=" ",
        options=options,
        index=idx,
        key=f"w_{qid}",
        label_visibility="collapsed",
    )


def render_app():
    st.title("Find Your Next Product Match!")
    init_state()

    try:
        stock_df = get_stock_df()
    except Exception as e:
        st.error("Failed to load stock CSV.")
        st.exception(e)
        st.stop()

    required_cols = {
        "Universe", "StoreCountry", "Category", "ProductType",
        "FamilyLevel1", "FamilyLevel2", "Quantity"
    }
    missing = required_cols - set(stock_df.columns)
    if missing:
        st.error(f"Stock file is missing required columns: {sorted(missing)}")
        st.stop()


    # RESULTS VIEW starts from here
    if st.session_state.result_df is not None:
        show_results_with_optional_images(st.session_state.result_df, "Top recommendations for you:")

        if st.session_state.client_id_verified:
            country_code = st.session_state.answers.get("country")
            customer_id = st.session_state.answers.get("customer_id", "")

            st.subheader("Products you may also like")

            try:
                catalog_df = get_catalog_df_for_country(country_code)

                if "ClientID" not in catalog_df.columns:
                    st.warning('Catalog file is missing required column "ClientID".')
                else:
                    cid = str(customer_id).strip()
                    matches = catalog_df[catalog_df["ClientID"].astype(str).str.strip() == cid]

                    if matches.empty:
                        st.warning("Client ID not found, please double check your ID, your country and region")
                    else:
                        row = matches.iloc[[0]]
                        if row.shape[1] < 8:
                            st.warning("Catalog does not contain enough recommendation columns.")
                        else:
                            recs = row.iloc[:, 3:8]
                            products = (
                                recs.iloc[0]
                                .dropna()
                                .astype(str)
                                .reset_index(drop=True)
                                .to_frame(name="product")
                            )
                            products["status"] = "Available"
                            show_results_with_optional_images(products, "Products you may also like")

            except Exception as e:
                st.warning("Could not load personalized recommendations.")
                st.exception(e)

        if not st.session_state.client_id_verified:
            st.markdown("---")
            st.subheader("Become a member today to enjoy customized service!")
            st.write(
                "Join our community to receive personalized recommendations, exclusive offers, "
                "and early access to new products."
            )

            email = st.text_input(
                "Sign up to our newsletter",
                placeholder="Enter your email address",
                key="newsletter_email",
            )

            if st.button("Sign up"):
                if email.strip() == "":
                    st.warning("Please enter a valid email address.")
                else:
                    st.success("Thank you for signing up! You'll receive our newsletter soon.")

        with st.expander("See your recorded answers"):
            st.json(st.session_state.answers)

        if st.button("Start over"):
            reset_quiz()
            st.rerun()

        return

    # QUESTION VIEW starts from here
    step = st.session_state.step
    choice = render_question(step)
    st.caption(f"Progress: {step + 1} / {len(QUESTIONS)}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Back", disabled=(step == 0)):
            st.session_state.step -= 1
            st.rerun()

    with col2:
        btn_label = "Next" if step < len(QUESTIONS) - 1 else "Finish"
        if st.button(btn_label):
            qid = QUESTIONS[step]["id"]
            prev = st.session_state.answers.get(qid)

            # Store answer (country label -> code)
            if qid == "country":
                st.session_state.answers[qid] = COUNTRIES[choice]
            else:
                st.session_state.answers[qid] = choice

            if prev is not None and prev != st.session_state.answers[qid]:
                clear_downstream_answers(qid)

            if qid == "customer_id":
                country_code = st.session_state.answers.get("country")
                ok, msg = verify_customer_id(country_code, str(choice))
                if not ok:
                    st.error(msg)
                    return
                st.session_state.client_id_verified = (str(choice).strip() != "")
                if msg:
                    st.success(msg)

            if step < len(QUESTIONS) - 1:
                st.session_state.step += 1
                st.rerun()
            else:
                try:
                    st.session_state.result_df = query_stock(stock_df, st.session_state.answers)
                except Exception as e:
                    st.error("SQL query failed.")
                    st.exception(e)
                    st.stop()
                st.rerun()

    if DEBUG_MODE:
        with st.expander("Debug (state)", expanded=False):
            st.json(st.session_state.answers)
            st.write("client_id_verified:", st.session_state.client_id_verified)
