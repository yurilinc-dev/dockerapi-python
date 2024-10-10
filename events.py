import docker
import datetime
import requests
import logging
import time
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

CHANNEL_ID = os.getenv('CHANNEL_ID')
WEBHOOK_ID = os.getenv('WEBHOOK_ID')
IP = os.getenv('IP')
PORT = os.getenv('PORT')

webhook_url = f"https://discord.com/api/webhooks/{CHANNEL_ID}/{WEBHOOK_ID}"

client = docker.DockerClient(base_url=f"tcp://{IP}:{PORT}")

while True:
    try:
        for event in client.events(decode=True, filters={"event": "die"}):
            try:
                container_id = event["id"]
                container_name = event["Actor"]["Attributes"]["name"]
                epoch_time = event["time"]
                date_time = datetime.datetime.utcfromtimestamp(epoch_time)

                payload = {
                    "content": f"O container {container_name} ({container_id}) foi finalizado às {date_time}"
                }

                logging.info(f"Payload: {payload}")
                response = requests.post(webhook_url, data=payload)

                if response.status_code != 204:
                    logging.error(f"Falha ao enviar webhook: {response.status_code} - {response.text}")

            except Exception as e:
                logging.error(f"Erro ao processar evento: {e}")

    except docker.errors.APIError as e:
        logging.error(f"Erro na API Docker: {e}")
        logging.info("Tentando reconectar em 5 segundos...")
        time.sleep(5)

    except Exception as e:
        logging.critical(f"Erro inesperado: {e}")
        break
