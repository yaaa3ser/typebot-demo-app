# Typebot Demo Web App

## Overview
This repository contains a Flask-based web application that integrates with the Typebot API to demonstrate a demo web app. 

The architecture consists of a Flask backend that handles authentication (mocked), bot listing, embedding, and analytics display. 

It uses a mocked token-based authentication system bridged to the Typebot API's Bearer token for API requests. 

The app fetches Typebot bots, embeds them via iframes, and displays basic analytics using API data.

## Architecture Overview
- **Frontend**: HTML templates (index.html, embed.html, analytics.html) with CSS.
- **Backend**: Flask Python app managing routes, API calls, and token validation.
- **Integration**: Typebot API for bot data, embedding, and analytics, with a mock bridge for authentication.
- **Data Flow**: API requests fetch bot lists and results, rendered into templates for user interaction.

## Setup Instructions
1. **Prerequisites**: Install Python 3.8+, pip, and virtualenv.
2. **Clone the Repository**:
```bash
git clone https://github.com/your-username/typebot-demo-app.git
cd typebot-demo-app
```
3. **Install Dependencies**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install flask requests python-dotenv
```
4. **Configure Environment**:
- Create a `.env` file in the project root:
TYPEBOT_API_TOKEN=your_api_token_here
TYPEBOT_WORKSPACE_ID=your_workspace_id_here

- Replace `your_api_token_here` and `your_workspace_id_here` with your Typebot API credentials.
5. **Run the App**:
```bash
python app.py
```

6. **Access**: Open `http://localhost:5000/?token=<VALID_TOKEN>` (use the token printed in the terminal).

## Tech Stack Used
- **Backend**: Python, Flask
- **Frontend**: HTML, CSS
- **API**: Typebot API (REST)
- **Dependencies**: requests, python-dotenv
- **Environment**: Virtual environment for dependency management

## API Usage or Postman Collection
- **List Bots**: `GET http://localhost:3000/api/v1/typebots?workspaceId={TYPEBOT_WORKSPACE_ID}`
    - Headers: `Authorization: Bearer {TYPEBOT_API_TOKEN}`
- **Embed Bot**: `GET http://localhost:3001/{bot_public_id}`
- **Get Bot Details**: `GET http://localhost:3000/api/v1/typebots/{bot_id}`
    - Headers: `Authorization: Bearer {TYPEBOT_API_TOKEN}`
- **Get Results**: `GET http://localhost:3000/api/v1/typebots/{bot_id}/results?limit=50&timeFilter=last7Days`
    - Headers: `Authorization: Bearer {TYPEBOT_API_TOKEN}`
- **use the above endpoints with a tool like Postman or curl for testing.**

## Known Limitations
- **Authentication**: Uses a mocked token system; real integration with Typebot auth would require a token exchange endpoint.
- **API Dependency**: Relies on the Typebot API, which may have rate limits or require a paid plan for full access.
- **User Tracking**: Does not currently save user answers to a database; requires webhook setup for user-specific data.
- **Iframe Embedding**: The iframe URL assumes a public Typebot instance; custom domains or session IDs may need adjustment.


## Future Enhancements
- **Real Authentication**: Implement OAuth or JWT for secure user authentication.
- **Database Integration**: Store user answers and bot interactions in a database for analytics.
- **Improved UI**: Enhance the frontend with better styling and user experience.
- **Error Handling**: Add robust error handling for API requests and user input validation.

## Demo
![Typebot Demo](./demo/demo.gif)