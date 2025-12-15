# Setup Guide

## Prerequisites

- Python 3.x
- `pip` (Python package installer)
- A GitHub Personal Access Token (optional, but recommended for higher rate limits and accurate pinned repos)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd github-user-getter
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Configuration:**
    Create a `.env` file in the root directory and add your GitHub token:
    ```
    GITHUB_TOKEN=your_token_here
    ```

## Running the Application

1.  Start the Flask server:
    ```bash
    python app.py
    ```

2.  Open your browser and navigate to:
    `http://127.0.0.1:5000`

## Deployment (Vercel)

You can easily deploy this Flask application to Vercel.

1.  **Install Vercel CLI:**
    ```bash
    npm install -g vercel
    ```

2.  **Create a `vercel.json` file** in the root directory:
    ```json
    {
      "version": 2,
      "builds": [
        {
          "src": "app.py",
          "use": "@vercel/python"
        }
      ],
      "routes": [
        {
          "src": "/(.*)",
          "dest": "app.py"
        }
      ]
    }
    ```

3.  **Deploy:**
    ```bash
    vercel
    ```

### Token Security & Public Release

For a public release, you might be concerned about exposing your `GITHUB_TOKEN`. 

**Good news:** Your current architecture is secure.
- The token is stored on the **server-side** (in your Flask app's environment).
- Users **never** see your token; they only communicate with your Flask app, which proxies requests to GitHub.

**Important:**
- **NEVER** commit your `.env` file to GitHub.
- When deploying to Vercel, go to your project settings -> **Environment Variables** and add `GITHUB_TOKEN` with your token value there. This allows the hosted app to use your token securely without exposing it in the code.

