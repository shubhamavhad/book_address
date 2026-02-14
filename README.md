**Setup & Run Instructions (Using uv)**
1.Install uv (If Not Installed)
 Windows (PowerShell)
pip install uv

OR (Recommended Method):
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

 Mac / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

Verify Installation
uv --version

2️.Install Dependencies

Make sure pyproject.toml exists in the root directory, then run:
uv sync

3️.Run the Application

Navigate to the folder where run.py is located and execute:
uv run run.py

**API Documentation**
Once the server is running, access the interactive API documentation:

🔹 Swagger UI
http://127.0.0.1:8000/docs

🔗 API Endpoints
1️.Create Address

POST /addresses

Request Body:
{
  "name": "Home",
  "street": "FC Road",
  "city": "Pune",
  "latitude": 18.5204,
  "longitude": 73.8567
}

2. Get Address

GET /addresses/{address_id}

Retrieves address details by ID.

3.Update Address (Partial Update Supported)

PUT /addresses/{address_id}

Only the provided fields will be updated.

Example:
{
  "city": "Mumbai"
}

4.Delete Address

DELETE /addresses/{address_id}
Deletes an address by ID.


FastAPI

uv (Python package manager & runner)
