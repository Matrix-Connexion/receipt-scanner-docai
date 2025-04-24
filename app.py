import os
import streamlit as st

# import yaml
# from utils.load_config import load_docai_config
from utils.process_receipt import process_receipt
from utils.display_data import display_receipt_data


def set_google_credentials_from_upload(key_file):
    try:
        key_path = "./tmp/service_account.json"
        with open(key_path, "wb") as f:
            f.write(key_file.read())
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
        st.session_state["google_credentials_path"] = key_path
        return True
    except Exception as e:
        st.error(f"Failed to set credentials from uploaded key: {e}")
        return False
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return False


# --- Main App ---
def main():
    st.set_page_config(page_title="Receipt Scanner", page_icon="🧾", layout="wide")
    app_ready = False

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
            if set_google_credentials_from_upload(key_file):
                st.success("Google credentials configured successfully.")
            else:
                st.error("Could not configure credentials.")
        else:
            st.warning("Please upload your Service Account JSON key.")

        with st.expander("How to configure"):
            st.markdown(
                f"""
            1.  **Create Document AI Processor:**
                ```
                google_cloud_project: "your-gcp-project-id"
                docai_location: "us" # e.g., us, eu
                docai_processor_id: "your-receipt-processor-id"
                service_account_key_path: "/full/path/to/your/keyfile.json" # Crucial!
                ```
            2.  **Get Credentials:**
                * Create/use a Google Cloud Project.
                * Enable Document AI API.
                * Create a 'Receipt Parser' processor, note its ID and Region (Location).
                * Create a Service Account, grant it the "Document AI User" role.
                * Download its JSON key file.
            3.  **Update `config.yaml`:** Fill in your project ID, location, processor ID, and the **full, correct path** to the downloaded JSON key file.
            4.  **Run App:** The script will attempt to use the `service_account_key_path` from the config to set the necessary environment variable automatically when it starts.
            """
            )

        st.title("About")
        st.info(
            "This app uses Google Cloud Document AI's Receipt Processor. "
            "It attempts to automatically configure credentials based on `config.yaml`."
        )
        st.title("Privacy")
        st.markdown(
            """
            - The app sets the `GOOGLE_APPLICATION_CREDENTIALS` environment variable for this session only to authenticate with Google Cloud.
            - We do not store your key file content or uploaded images.
            - Processing is done via your configured Google Cloud Document AI processor.
            """
        )

    if (
        "google_credentials_path" in st.session_state
        and project_id
        and location
        and processor_id
    ):
        app_ready = True
        st.success("App is ready to process receipts. Upload a receipt to proceed.")

    if not app_ready:
        st.info(
            "Please configure Google Cloud Document AI project id, document AI processor location, processor and upload your service account key at the sidebar"
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

    if uploaded_file and app_ready:
        st.image(uploaded_file, caption="Uploaded Document", use_column_width=True)
        if st.button("Process Document"):
            with st.spinner("Processing with Document AI..."):
                receipt_data = process_receipt(
                    uploaded_file, project_id, location, processor_id
                )
                display_receipt_data(receipt_data)


if __name__ == "__main__":
    main()
