import os
import json
import requests
import logging
from datetime import datetime, timedelta
from notion_client import Client as NotionClient
from dateutil import parser
import time
from dotenv import load_dotenv
# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("sync_log.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger()

def clean_project_ids(project_ids_str):
    # Elimina caracteres no deseados y divide por comas
    cleaned_ids = project_ids_str.replace("[", "").replace("]", "").replace("'", "").replace(" ", "").replace("\"","")
    return cleaned_ids.split(",")
load_dotenv()
# Leer variables de entorno
ticktick_access_token = os.getenv('TICKTICK_ACCESS_TOKEN')
notion_token = os.getenv('NOTION_TOKEN')
notion_database_id = os.getenv('NOTION_DATABASE_ID')
project_ids = clean_project_ids(os.getenv('PROJECT_IDS'))
sync_interval = float(os.getenv('SYNC_INTERVAL', 300))

# Cliente de Notion
print(ticktick_access_token)

notion = NotionClient(auth=notion_token)

def read_processed_tasks(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.warning(f"El archivo {file_path} no fue encontrado. Se creará uno nuevo.")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Error al decodificar el JSON en el archivo {file_path}.")
        return {}

def write_processed_tasks(file_path, processed_tasks):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(processed_tasks, file)
    logger.info("Registro de tareas procesadas actualizado.")

def get_tasks_from_project(project_id):
    url = f'https://api.ticktick.com/open/v1/project/{project_id}/data'
    print(url)
    headers = {
        'Authorization': f'Bearer {ticktick_access_token}',
        'Cookie': 'AWSALB=INSERT_YOUR_COOKIE_HERE',  # Update this if necessary
        'User-Agent': 'PostmanRuntime/7.37.3',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            tasks = response.json()['tasks']
            logger.info(f"Tareas obtenidas correctamente del proyecto {project_id}.")
            return tasks
        except KeyError:
            print(f" No hay tareas dentro del proyecto {project_id}: {response.json()}")
        except Exception as e:
            logger.error(f"Error al obtener tareas del proyecto {project_id}: {e}")
        
        
    else:
        logger.error(f"Error {response.status_code} al obtener tareas del proyecto {project_id}: {response.text}")
        return []

def add_task_to_notion(title, description, start_date):
    try:
        end_date = start_date + timedelta(hours=1)
        new_page_data = {
            "parent": {"database_id": notion_database_id},
            "properties": {
                "Name": {"title": [{"text": {"content": title}}]},
                "Description": {"rich_text": [{"text": {"content": description}}]},
                "Date": {"date": {"start": start_date.isoformat(), "end": end_date.isoformat()}}
            }
        }
        notion.pages.create(**new_page_data)
        logger.info(f"Tarea '{title}' añadida a Notion.")
    except Exception as e:
        logger.error(f"Error al añadir tarea a Notion: {e}")

def sync_tasks_to_notion(project_ids):
    processed_tasks = read_processed_tasks('processed_tasks.json')
    for project_id in project_ids:
        tasks = get_tasks_from_project(project_id)
        if not tasks: continue
        for task in tasks:
            try:  # Try block to catch and log errors per task
                task_id = task['id']
                if task_id not in processed_tasks:
                    if 'startDate' not in task:
                        logger.warning(f"La tarea '{task['title']}' no tiene 'startDate' y será omitida.")
                        continue
                    start_date = parser.parse(task['startDate'])
                    
                    add_task_to_notion(task['title'], task.get('content', ""), start_date)
                    
                    processed_tasks[task_id] = True
                    logger.info(f"Tarea '{task['title']}' procesada y registrada.")
            except Exception as e:
                logger.error(f"Error al procesar la tarea '{task.get('title', 'Unknown Title')}': {e}")

    write_processed_tasks('processed_tasks.json', processed_tasks)

if __name__ == "__main__":
    # Run the sync process every 'sync_interval' seconds
    while True:
        sync_tasks_to_notion(project_ids)
        logger.info(f"Waiting {sync_interval} seconds until the next sync.")
        time.sleep(sync_interval)