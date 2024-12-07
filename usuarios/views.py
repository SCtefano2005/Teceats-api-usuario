from rest_framework.response import Response
from rest_framework.decorators import api_view
from requests_oauthlib import OAuth2Session
from decouple import config
import requests
from .models import Usuario, DueñoRestaurante
from .serializers import UsuarioSerializer, DueñoRestauranteSerializer

# Configuración de OAuth 2
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"
SCOPES = ["https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]
GOOGLE_CLIENT_ID = config("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = config("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI_USUARIO = config("GOOGLE_REDIRECT_URI_USUARIO")
GOOGLE_REDIRECT_URI_DUENO = config("GOOGLE_REDIRECT_URI_DUENO")

def get_oauth_session(redirect_uri):
    return OAuth2Session(GOOGLE_CLIENT_ID, redirect_uri=redirect_uri, scope=SCOPES)

@api_view(["GET"])
def google_login_usuario(request):
    oauth = get_oauth_session(GOOGLE_REDIRECT_URI_USUARIO)
    auth_url, state = oauth.authorization_url(GOOGLE_AUTH_URL, access_type="offline", prompt="consent")
    request.session["oauth_state"] = state
    return Response({"auth_url": auth_url})

@api_view(["GET"])
def google_login_dueno(request):
    oauth = get_oauth_session(GOOGLE_REDIRECT_URI_DUENO)
    auth_url, state = oauth.authorization_url(GOOGLE_AUTH_URL, access_type="offline", prompt="consent")
    request.session["oauth_state"] = state
    return Response({"auth_url": auth_url})

@api_view(["GET"])
def google_callback_usuario(request):
    return _handle_google_callback(request, GOOGLE_REDIRECT_URI_USUARIO, Usuario)

@api_view(["GET"])
def google_callback_dueno(request):
    return _handle_google_callback(request, GOOGLE_REDIRECT_URI_DUENO, DueñoRestaurante)

def _handle_google_callback(request, redirect_uri, user_model):
    try:
        oauth = OAuth2Session(GOOGLE_CLIENT_ID, state=request.session.get("oauth_state"), redirect_uri=redirect_uri)
        token = oauth.fetch_token(
            GOOGLE_TOKEN_URL,
            client_secret=GOOGLE_CLIENT_SECRET,
            authorization_response=request.build_absolute_uri(),
        )
        user_info = requests.get(
            GOOGLE_USER_INFO_URL,
            headers={"Authorization": f'Bearer {token["access_token"]}'},
        ).json()

        google_id = user_info.get("id")
        email = user_info.get("email")
        name = user_info.get("name")

        # Restricción de dominio para usuarios
        if user_model == Usuario and not email.endswith("@tecsup.edu.pe"):
            return Response({"error": "Acceso denegado. Solo se permiten correos @tecsup.edu.pe."}, status=403)

        # Crear o actualizar el usuario
        user, created = user_model.objects.update_or_create(
            google_id=google_id,
            defaults={
                "nombre": name,
                "correo_electronico": email,
                "token_acceso": token.get("access_token"),
                "token_refresh": token.get("refresh_token"),
            },
        )

        # Serializar y devolver los datos
        serializer = UsuarioSerializer(user) if user_model == Usuario else DueñoRestauranteSerializer(user)
        return Response(serializer.data, status=201 if created else 200)

    except Exception as e:
        return Response({"error": str(e)}, status=400)
