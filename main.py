
import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = 'https://www.bettingpros.com/mlb/player-prop-bets/'

def enviar_mensaje(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": mensaje}
    try:
        requests.post(url, data=data)
    except:
        pass

def calcular_ev(probabilidad, cuota):
    return (probabilidad * cuota) - 1

def extraer_datos():
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        filas = soup.select('tr.propbets__table-row')
        for fila in filas:
            nombre = fila.select_one('.propbets__table-player-name').text.strip()
            mercado = fila.select_one('.propbets__table-stat-type').text.strip()
            prob = float(fila.select_one('.probability-text').text.strip('%')) / 100
            cuota = float(fila.select_one('.american').text.strip('+–').replace(',', '.'))

            if cuota >= 1.60 and prob >= 0.70:
                ev = calcular_ev(prob, cuota)
                if ev > 0:
                    mensaje = f"⚾️ UNDER EV+ DETECTADO\n\nJugador: {nombre}\nMercado: {mercado}\nProb: {prob*100:.1f}%\nCuota: {cuota}\nEV: {ev:.2f}"
                    enviar_mensaje(mensaje)
    except Exception as e:
        pass

if __name__ == "__main__":
    extraer_datos()
