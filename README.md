# Receipt Scanner

A web application that uses Google's Gemini API to scan receipts and extract structured information. The application allows users to upload receipt images, processes them using OCR and AI, and displays the extracted information in a structured format.

## Features

- Upload receipt images in common formats (JPG, PNG)
- Extract merchant details, transaction information, line items, and financial data
- Display structured receipt data in a user-friendly format
- View raw JSON data for integration with other systems
- Deployed as a containerized application on Google Cloud Run
- User-provided Gemini API key for processing

## Architecture

This application uses:

- **FastAPI**: Main web server framework
- **Uvicorn**: ASGI server for running the FastAPI application
- **Streamlit**: Interactive UI framework embedded within the FastAPI application
- **Google Gemini API**: AI model for OCR and information extraction

## Project Structure

```
receipt-scanner/
│
├── app/
│   ├── __init__.py
│   ├── main.py                # Streamlit application
│   ├── server.py              # FastAPI server
│   ├── utils.py               # Utility functions
│   └── health_check.py        # Health check utility
│
├── templates/
│   └── index.html             # HTML template for embedding Streamlit
│
├── static/
│   └── style.css              # Custom CSS
│
├── .dockerignore              # Files to exclude from Docker build
├── .gitignore                 # Files to exclude from Git
├── .gcloudignore              # Files to exclude from Google Cloud deployments
├── Dockerfile                 # Container configuration
├── requirements.txt           # Python dependencies
├── cloudbuild.yaml            # Cloud Build configuration
├── deploy.py                  # Deployment script
└── run_local.py               # Local development script
```

## Prerequisites

- Python 3.9+
- Docker (for local container testing)
- Google Cloud SDK (for deployment)
- Google Gemini API key (users will need to obtain their own key)

## Local Development

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/receipt-scanner.git
   cd receipt-scanner
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Make the scripts executable:
   ```bash
   chmod +x deploy.py run_local.py
   ```

### Running Locally

Run the application with:

```bash
./run_local.py
```

Optional arguments:
- `--port`: Port to run the server on (default: 8080)
- `--streamlit-port`: Port for Streamlit (default: 8501)
- `--reload`: Enable auto-reload for development

Then open your browser to http://localhost:8080

### Docker Build

Build and run the Docker container locally:

```bash
docker build -t receipt-scanner .
docker run -p 8080:8080 receipt-scanner
```

## Deployment to Google Cloud Run

### Prerequisites

1. Install the Google Cloud SDK
2. Initialize and configure gcloud:
   ```bash
   gcloud init
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. Enable required APIs:
   ```bash
   gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com
   ```

4. Create an Artifact Registry repository:
   ```bash
   gcloud artifacts repositories create receipt-scanner --repository-format=docker --location=us-central1 --description="Receipt Scanner Docker repository"
   ```

5. Configure Docker to authenticate with Artifact Registry:
   ```bash
   gcloud auth configure-docker us-central1-docker.pkg.dev
   ```

### Deployment

Deploy using the provided script:

```bash
./deploy.py
```

Optional arguments:
- `--region`: Google Cloud region to deploy to (default: us-central1)
- `--tag`: Image tag to use (default: latest)
- `--memory`: Memory allocation for Cloud Run instance (default: 512Mi)
- `--cpu`: CPU allocation for Cloud Run instance (default: 1)

### Continuous Deployment with Cloud Build

Set up continuous deployment using Cloud Build:

```bash
gcloud builds submit --config=cloudbuild.yaml
```

## Usage

1. Open the application in your browser
2. Enter your Gemini API Key in the sidebar
   - You'll need to obtain a key from [Google AI Studio](https://aistudio.google.com)
3. Upload a receipt image
4. Click "Process Receipt"
5. View the extracted information

## Getting a Gemini API Key

To use this application, you'll need a Google Gemini API key:

1. Go to [Google AI Studio](https://aistudio.google.com)
2. Sign in with your Google account
3. Navigate to the API keys section
4. Create a new API key
5. Copy the key and paste it in the application when prompted

## Environment Variables

- `PORT`: Port for the FastAPI server (default: 8080)
- `STREAMLIT_PORT`: Port for the Streamlit application (default: 8501)

## Security Considerations

- The Gemini API key is entered by the user and is not stored on the server
- The key is only used for the current session and is not persisted
- Consider adding authentication for the application in production environments

## Troubleshooting

### Common Issues

1. **Application not starting**: Check the logs with `docker logs` or Cloud Run logs
2. **API key errors**: Verify your Gemini API key is correct and has the necessary permissions
3. **Image processing errors**: Ensure the receipt image is clear and in a supported format

### Health Check

Run the health check utility to verify the application is running correctly:

```bash
python -m app.health_check --url http://localhost:8080
```

## License

[MIT License](LICENSE)

## Acknowledgements

- Google Gemini API for OCR and information extraction
- Streamlit for the interactive UI components
- FastAPI for the web server framework

---

For questions or support, please open an issue on the GitHub repository.