Setup & Run Instructions (Using uv)

1.Install uv (If Not Installed)

Windows (PowerShell):
pip install uv
OR (recommended method):
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

Mac/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

Verify installation:
uv --version

2.Install Dependencies

pyproject.toml exists:
uv sync

3.Run the Application

Please run the below command in the folder where the run.py file is present:
uv run run.py





API Documentation

After starting the server:

Swagger UI:
http://127.0.0.1:8000/docs

API Endpoints
1.Create Address

POST /addresses

{
  "name": "Home",
  "street": "FC Road",
  "city": "Pune",
  "latitude": 18.5204,
  "longitude": 73.8567
}

2. Get Address

GET /addresses/{address_id}

3. Update Address (Partial Update Supported)

PUT /addresses/{address_id}

Example:

{
  "city": "Mumbai"
}


Only provided fields will be updated.

4.Delete Address

DELETE /addresses/{address_id}
