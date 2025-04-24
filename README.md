# Receipt Scanner with Google Document AI
A web application that uses Google Cloud Document AI to scan receipts and extract structured information. The application allows users to upload receipt images, processes them using Google's Document AI Receipt Parser, and displays the extracted information in a structured format.

## Features
Upload receipt images in common formats (JPG, PNG)
Extract merchant details, transaction information, line items, and financial data using Google Document AI
Display structured receipt data in a user-friendly format
Secure credential management with Google Cloud service accounts
Easy configuration through the UI or config file
Prerequisites
Python 3.9+
Google Cloud account with Document AI API enabled
Document AI Receipt Parser processor
Service account with "Document AI User" role
Setup
Clone the repository:

```
git clone https://github.com/yourusername/receipt-scanner-docai.git
cd receipt-scanner-docai
```

Execute

Create a virtual environment and install dependencies:

```
python -m venv venv
```
```
source venv/bin/activate
```  # On Windows: venv\Scripts\activate
```
pip install -r requirements.txt
```

Execute

Configure Google Cloud Document AI:

Create/use a Google Cloud Project
Enable Document AI API
Create a 'Receipt Parser' processor, note its ID and Region (Location)
Create a Service Account, grant it the "Document AI User" role
Download its JSON key file
Update config.yaml with your Google Cloud settings:

google_cloud:
  project_id: "your-gcp-project-id"
  location: "us"  # or "eu" depending on your processor location
  processor_id: "your-receipt-processor-id"
  service_account_key_path: "/full/path/to/your/keyfile.json"



Running the Application
Run the application with:

streamlit run app.py

Execute

Then open your browser to the URL provided by Streamlit (typically http://localhost:8501)

Usage
Open the application in your browser
If not configured via config.yaml, enter your Google Cloud settings in the sidebar:
Project ID
Location (e.g., "us" or "eu")
Processor ID
Upload your service account key file
Upload a receipt image
View the extracted information
Security Considerations
The application sets the GOOGLE_APPLICATION_CREDENTIALS environment variable for the current session only
Service account key files are not stored permanently when uploaded through the UI
Processing is done via your configured Google Cloud Document AI processor
Consider adding authentication for the application in production environments
Troubleshooting
Common Issues
Credential errors: Ensure your service account key file has the correct permissions and is accessible
API not enabled: Verify that Document AI API is enabled in your Google Cloud project
Processor configuration: Check that your processor ID and location are correct
Image processing errors: Ensure the receipt image is clear and in a supported format
License
MIT License

Acknowledgements
Google Cloud Document AI for receipt parsing
Streamlit for the interactive UI components
For questions or support, please open an issue on the GitHub repository.