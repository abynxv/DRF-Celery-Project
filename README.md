# Django Celery Task Project

This project demonstrates **asynchronous task processing** using **Django, Celery, and Redis**.  
It currently includes basic arithmetic tasks (`add` and `multiply`) and APIs to fetch task results.  
Future features will be added as the project evolves.

📌 Project Status

> Basic arithmetic tasks implemented.

> Future features and improvements will be added (periodic tasks, advanced routing, monitoring, etc.)

---

## Tech Stack

- **Django** – Web framework  
- **Django REST Framework (DRF)** – API development  
- **Celery** – Distributed task queue  
- **Redis** – Broker and result backend  

---

## Setup Instructions

### Clone the Repository
```bash
git clone <repo-url>
cd <project-folder>
```
### Create Virtual Environment & Activate
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```
### Install Requirements
```bash
pip install -r requirements.txt
```
### Start Redis Server
Make sure Redis is installed and running:
```bash
redis-server
```
### Apply Migrations and Run Django Server
```bash
python manage.py migrate
python manage.py runserver
```
### Start Celery Worker
Open another terminal and run:
```bash
celery -A drf_celery_project worker --loglevel=info
```
<img width="1281" height="734" alt="Screenshot from 2025-08-01 12-52-24" src="https://github.com/user-attachments/assets/570ab39f-0e54-4e4a-83d1-145e62dd1a4b" />

### API Endpoints - Trigger Tasks
Add Numbers: POST /add/
```bash
Body:
{
  "a": 10,
  "b": 20
}
```
<img width="1329" height="553" alt="Screenshot from 2025-08-01 12-47-14" src="https://github.com/user-attachments/assets/dcd5827f-2a08-4658-9ffb-04a6c3e8d1f3" />
Multiply Numbers: POST /multiply/
```bash
Body:
{
  "a": 5,
  "b": 6
}
```
<img width="1329" height="553" alt="Screenshot from 2025-08-01 12-47-28" src="https://github.com/user-attachments/assets/71086adc-5a55-4809-8793-20d575d5fdf3" />
## Fetch Task Results
```bash
List All Results: GET /results/
```
<img width="1329" height="522" alt="Screenshot from 2025-08-01 12-48-05" src="https://github.com/user-attachments/assets/b1366c7b-c2ea-40fc-bc40-fae2a179c282" />
```
```bash
Get Specific Result: GET /results/<task_id>/
```
<img width="1329" height="522" alt="Screenshot from 2025-08-01 12-48-12" src="https://github.com/user-attachments/assets/80de94b8-1915-496f-b190-a7b063ca8231" />
