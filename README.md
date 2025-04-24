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
source venv/bin/activate # On Windows: venv\Scripts\activate
```  
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
```
pip install -r requirements.txt
```


## Configure Google Cloud Document AI:

1. Create/use a Google Cloud Project
2. Enable Document AI API
3. Create a 'Receipt Parser' processor, note its ID and Region (Location)
4. Create a Service Account, grant it the "Document AI User" role
5. Download its JSON key file

Running the Application locally:

1. Clone this repository
   ```
   git clone
   ```
2. Run the app

  ```
  streamlit run app.py
  ```

<<<<<<< Updated upstream
3. Then open your browser to the URL provided by Streamlit (typically http://localhost:8501)

## Usage
=======
## Running the Application
Run the application with:

```
streamlit run app.py
```


Then open your browser to the URL provided by Streamlit (typically http://localhost:8501)

Usage
>>>>>>> Stashed changes
Open the application in your browser
Enter your Google Cloud settings in the sidebar:
1. Project ID
2. Location (e.g., "us" or "eu")
3. Processor ID
4. Upload your service account key file
5. Upload a receipt image
6. View the extracted information
   
## Security Considerations
1. The application sets the GOOGLE_APPLICATION_CREDENTIALS environment variable for the current session only
2. Service account key files are not stored permanently when uploaded through the UI
3. Processing is done via your configured Google Cloud Document AI processor
4. Consider adding authentication for the application in production environments

## Troubleshooting
### Common Issues
1. Credential errors: Ensure your service account key file has the correct permissions and is accessible
2. API not enabled: Verify that Document AI API is enabled in your Google Cloud project
3. Processor configuration: Check that your processor ID and location are correct
4. Image processing errors: Ensure the receipt image is clear and in a supported format

## Acknowledgements
1. Google Cloud Document AI for receipt parsing
2. Streamlit for the interactive UI components

For questions or support, please open an issue on the GitHub repository.
