import os
import streamlit as st
from utils.process_receipt import process_receipt
from utils.display_data import display_receipt_data
from google.oauth2 import service_account
import json


def get_credentials_from_upload(key_file):
    try:
        key_json = json.load(key_file)
        credentials = service_account.Credentials.from_service_account_info(key_json)
        return credentials, key_json
    except Exception as e:
        st.error(f"Failed to load service account: {e}")
        return None, None


# --- Main App ---
def main():
    st.set_page_config(page_title="Receipt Scanner", page_icon="🧾", layout="wide")
    st.title("Receipt Scanner")
    st.markdown("Upload a receipt image to extract structured data using Document AI.")

    # --- Sidebar Configuration Inputs ---
    with st.sidebar:
        st.header("🔧 Document AI Configuration")
        project_id = st.text_input("Project ID", value="your-gcp-project-id")
        location = st.selectbox("Location (e.g. us, eu)", options=["us", "eu"])
        processor_id = st.text_input("Processor ID", value="your-receipt-processor-id")

        key_file = st.file_uploader("Upload Service Account Key (JSON)", type=["json"])
        if key_file:
            credentials, key_info = get_credentials_from_upload(key_file)
            if credentials:
                st.session_state["google_credentials"] = credentials
                st.session_state["project_id"] = project_id or key_info.get("project_id")
                st.session_state["location"] = location
                st.session_state["processor_id"] = processor_id
                st.success("Google credentials configured successfully.")
            else:
                st.error("Could not configure credentials.")
        else:
            st.warning("Please upload your Service Account JSON key.")

        with st.expander("How to configure"):
            st.markdown(
                """
                1.  **Create Document AI Processor** in your GCP project.
                2.  **Enable the Document AI API**.
                3.  **Create a Service Account** with "Document AI User" role.
                4.  **Download the JSON key file** and upload it here.
                5.  Provide the Project ID, Processor Location, and Processor ID.
                """
            )

        st.title("About")
        st.info(
            "This app uses Google Cloud Document AI's Receipt Processor. "
            "Your key file is used only during this session and not stored."
        )

    app_ready = all([
        "google_credentials" in st.session_state,
        st.session_state.get("project_id"),
        st.session_state.get("location"),
        st.session_state.get("processor_id")
    ])

    if not app_ready:
        st.info(
            "Please configure the Document AI settings and upload your service account key to continue."
        )
        st.stop()

    try:
        from google.cloud import documentai
    except ImportError:
        st.error(
            "Missing `google-cloud-documentai` library. Install via `pip install google-cloud-documentai`."
        )
        st.stop()

    # --- File Upload & Processing ---
    uploaded_file = st.file_uploader(
        "Choose a receipt (.jpg, .png, .pdf, .tif)...",
        type=["jpg", "jpeg", "png", "pdf", "tif", "tiff"],
    )

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Document", use_column_width=True)
        if st.button("Process Document"):
            with st.spinner("Processing with Document AI..."):
                receipt_data = process_receipt(
                    uploaded_file,
                    st.session_state["google_credentials"],
                    st.session_state["project_id"],
                    st.session_state["location"],
                    st.session_state["processor_id"]
                )
                display_receipt_data(receipt_data)


if __name__ == "__main__":
    main()