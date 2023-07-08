import requests
import websocket
from urllib3.exceptions import InsecureRequestWarning

from msp import invoke_method, get_session_id, ticket_header, Actor, connect_websocket
import warnings



# Définir les informations de connexion
USERNAME = "*****"
PASSWORD = "*****"
SERVER = "FR"

# Appeler la méthode de connexion et obtenir la réponse
code, resp = invoke_method(
    SERVER,
    "MovieStarPlanet.WebService.User.AMFUserServiceWeb.Login",
    [
        USERNAME,
        PASSWORD,
        [],
        None,
        None,
        "MSP1-Standalone:XXXXXX"
    ],
    get_session_id()
)

print(resp)  # Affiche le contenu de la variable resp

if resp is None:
    print("La méthode d'authentification a renvoyé None. Vérifiez les paramètres d'authentification.")
    quit()

# Vérifier si la connexion a réussi
status = resp.get('loginStatus', {}).get('status')
if status != "Success":
    print(f"Login failed, status: {status}")
    quit()

ticket = resp['loginStatus']['ticket']
actor_id = resp['loginStatus']['actor']['ActorId']

nebula_id = resp['loginStatus']['nebulaLoginStatus']['profileId']
nebula_token = resp['loginStatus']['nebulaLoginStatus']['accessToken']
actor = Actor(SERVER, nebula_id, nebula_token)
connect_websocket(actor)

name = "*****"
code, resp = invoke_method(
    SERVER,
    "MovieStarPlanet.WebService.AMFActorService.GetActorIdByName",
    [
        ticket_header(ticket),
        name
    ],
    get_session_id()
)
receiverActorId = resp
code, resp = invoke_method(
    SERVER,
    "MovieStarPlanet.WebService.UserSession.AMFUserSessionService.GiveAutographAndCalculateTimestamp",
    [
        ticket_header(ticket),
        actor_id,
        receiverActorId
    ],
    get_session_id()
)

print(resp, code)
