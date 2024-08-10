# AngelCam Web View

AngelCam Web View is a Django project that provides a web interface for interacting with AngelCam's camera and recording APIs. This project allows users to manage cameras, access recording timelines, and control recordings.

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [API Endpoints](#api-endpoints)
   - [Accounts](#accounts)
   - [Cameras](#cameras)
4. [Usage](#usage)

## Installation

**Clone the Repository**

```bash
git clone https://github.com/yourusername/angelcam-web-view.git
cd angelcam-web-view
```
**Create and Activate a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate
```

**Install Dependencies**
```bash
pip install -r requirements.txt
```

**Apply Migrations**
```bash
python manage.py migrate
```

**Run the Development Server**
```bash
python manage.py runserver
```

## Docker

### Build and Run the Docker Container

To deploy the project using Docker, follow these steps:

**Build the Docker Image**

```bash
docker-compose up --build
```
## API Endpoints
**Accounts**
- **Login**: `/api/accounts/login`
  - **Method**: `POST`
  - **Description**: Logs in a user.

### Cameras

- **List Cameras**: `/api/cameras/cameras/`
  - **Method**: `GET`
  - **Description**: Retrieves a list of all cameras.

- **Camera Detail**: `/api/cameras/camera/<int:camera_id>`
  - **Method**: `GET`
  - **Description**: Retrieves detailed information for a specific camera.

- **Recording Info**: `/api/cameras/camera/<str:camera_id>/recording/info`
  - **Method**: `GET`
  - **Description**: Retrieves recording information for a specific camera.

- **Recording Timeline**: `/api/cameras/camera/<str:camera_id>/recording/timeline`
  - **Method**: `GET`
  - **Description**: Retrieves the recording timeline for a specific camera.
  - **Query Parameters**:
    - `start` (optional): Start date and time in ISO 8601 format.
    - `end` (optional): End date and time in ISO 8601 format.

- **Recording Stream**: `/api/cameras/camera/<str:camera_id>/recording/stream`
  - **Method**: `GET`
  - **Description**: Retrieves the recording stream URL for a specific camera.
  - **Query Parameters**:
    - `start` (optional): Start date and time in ISO 8601 format.

- **Play Recording**: `/api/recording/<str:domain>/<str:stream_id>/play`
  - **Method**: `POST`
  - **Description**: Starts playing a recording stream.

- **Pause Recording**: `/api/recording/<str:domain>/<str:stream_id>/pause`
  - **Method**: `POST`
  - **Description**: Pauses the recording stream.

- **Speed Recording**: `/api/recording/<str:domain>/<str:stream_id>/speed`
  - **Method**: `POST`
  - **Description**: Adjusts the speed of the recording stream.
  - **Request Body**:
    ```json
    {
      "speed": 1.0
    }
    ```

## Usage

- **Login**: Use the `/api/accounts/login` endpoint to obtain a token.
- **Manage Cameras**: Use the `/api/cameras/` endpoints to interact with camera data.
- **Control Recordings**: Use the `/api/recording/` endpoints to control and get information about recordings.

