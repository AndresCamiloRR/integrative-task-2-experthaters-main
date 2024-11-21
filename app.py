import os

def run_pip_commands():
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    os.system("pip install experta")
    os.system("pip install --upgrade frozendict")
    os.system("pip uninstall -y frozendict")
    os.system("pip uninstall -y yfinance")
    os.system("pip install yfinance")

# Run the pip commands
run_pip_commands()

import streamlit as st
from dotenv import load_dotenv
import psycopg2
import bcrypt
import jwt
import uuid
from datetime import datetime, timedelta, timezone
import json
from weird_noises_problem_bn import get_ruidos_problems_response
from electric_problems_bn import get_electric_problems_response

load_dotenv()
st.title("Chatbot For Car Troubleshooting")

# Database connection
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
cursor = conn.cursor()

# JWT secret key
JWT_SECRET = os.getenv("JWT_SECRET")

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_jwt(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def decode_jwt(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None

def get_user_by_email(email):
    cursor.execute("SELECT id, password FROM users WHERE email = %s", (email,))
    return cursor.fetchone()

def get_user_by_id(user_id):
    cursor.execute("SELECT email FROM users WHERE id = %s", (user_id,))
    return cursor.fetchone()

def create_user(email, password):
    hashed_password = hash_password(password)
    cursor.execute(
        "INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
    conn.commit()

def save_chat_to_db(user_id, chat_id, messages):
    messages_json = json.dumps(messages)
    cursor.execute(
        "INSERT INTO chats (user_id, chat_id, messages) VALUES (%s, %s, %s) ON CONFLICT (chat_id) DO UPDATE SET messages = %s",
        (user_id, chat_id, messages_json, messages_json)
    )
    conn.commit()

def get_welcome_message(network):
    if network == "r":
        return "¡Bienvenido al diagnóstico de r extraños! Voy a hacerte algunas preguntas para ayudarte a identificar el origen de los r. Por favor, responde 's' para sí o 'n' para no."
    elif network == "e":
        return "¡Bienvenido al diagnóstico de problemas eléctricos! Voy a hacerte algunas preguntas para ayudarte a identificar posibles fallas. Por favor, responde 's' para sí o 'n' para no."
    return ""

def get_bayesian_response(responses):
    if st.session_state.selected_network == "r":
        return get_ruidos_problems_response(responses)
    elif st.session_state.selected_network == "e":
        return get_electric_problems_response(responses)
    else:
        return "Por favor selecciona una red bayesiana para iniciar el diagnóstico."

def load_chat_from_db(user_id, chat_id):
    cursor.execute(
        "SELECT messages FROM chats WHERE user_id = %s AND chat_id = %s", (user_id, chat_id))
    result = cursor.fetchone()
    return result[0] if result else []

def load_all_chats_from_db(user_id):
    cursor.execute("SELECT chat_id FROM chats WHERE user_id = %s", (user_id,))
    return [row[0] for row in cursor.fetchall()]

def get_first_prompt(user_id, chat_id):
    messages = load_chat_from_db(user_id, chat_id)
    for message in messages:
        if message["role"] == "assistant":
            return message["content"]
    return "No prompt"

@st.dialog("Login")
def login_dialog():
    st.write("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button(" Login "):
        user = get_user_by_email(email)
        if user and check_password(password, user[1]):
            st.session_state.jwt = create_jwt(user[0])
            st.session_state.selected_network = "n"
            st.query_params = {"jwt": st.session_state.jwt, "selected_network": "n"}
            st.rerun()
        else:
            st.error("Invalid credentials")

@st.dialog("Sign Up")
def signup_dialog():
    st.write("Sign Up")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button(" Sign Up "):
        if get_user_by_email(email):
            st.error("Email already registered")
        else:
            create_user(email, password)
            st.success("User created successfully. Please log in.")

# Initialize additional session states
if "jwt" not in st.session_state:
    st.session_state.jwt = None

if 'selected_network' not in st.session_state:
    st.session_state.selected_network = None

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'responses' not in st.session_state:
    st.session_state.responses = []

if 'question_index' not in st.session_state:
    st.session_state.question_index = 0

if 'user_id' not in st.session_state:
    st.session_state.user_id = None

if 'chat_id' not in st.session_state:
    st.session_state.chat_id = None

if 'welcomed' not in st.session_state:
    st.session_state.welcomed = False

# Check for JWT and selected_network in query parameters
query_params = st.query_params
if "jwt" in query_params and query_params["jwt"] is not None:
    st.session_state.jwt = query_params["jwt"]

if "selected_network" in query_params and query_params["selected_network"] is not None:
    st.session_state.selected_network = query_params["selected_network"]


# Authentication
if st.session_state.jwt:
    try:
        decoded = decode_jwt(st.session_state.jwt)
        if decoded:
            st.session_state.user_id = decoded["user_id"]
            # Update query parameters to include JWT
            st.query_params = {"jwt": st.session_state.jwt}
        else:
            raise jwt.DecodeError
    except jwt.DecodeError:
        st.session_state.jwt = None
        st.session_state.user_id = None
        st.session_state.chat_id = None
        st.session_state.messages = []
        st.session_state.welcomed = False
        # Clear query parameters
        st.query_params = {}

# Sidebar with login/logout and chat options
with st.sidebar:
    if st.session_state.user_id:
        user_email = get_user_by_id(st.session_state.user_id)[0]
        st.text(f"Logged in as: {user_email}")
        if st.button("Logout"):
            st.session_state.jwt = None
            st.session_state.chat_id = None
            st.session_state.messages = []
            st.query_params = {}  # Clear query parameters
            st.rerun()

        st.write("Chats")
        chat_ids = load_all_chats_from_db(st.session_state.user_id)
        for cid in chat_ids:
            first_prompt = get_first_prompt(st.session_state.user_id, cid)
            if st.button(first_prompt, key=cid):
                st.session_state.chat_id = cid
                st.session_state.messages = load_chat_from_db(st.session_state.user_id, cid)
                st.rerun()

        if st.button("Create New Chat"):
            st.session_state.chat_id = None
            st.session_state.messages = []
            st.session_state.welcomed = False
            st.session_state.network_selected = False
            st.query_params = {"jwt": st.session_state.jwt, "selected_network": "n"}
            st.rerun()

        #if st.button("Delete Current Chat") and st.session_state.chat_id:
        #    st.session_state.chat_id = None
        #    st.session_state.messages = []
        #    st.session_state.welcomed = False
        #    st.session_state.network_selected = False
        #    st.query_params = {"jwt": st.session_state.jwt, "selected_network": "n"}
        #    cursor.execute("DELETE FROM chats WHERE user_id = %s AND chat_id = %s",
        #                   (st.session_state.user_id, st.session_state.chat_id))
        #    conn.commit()
        #    st.rerun()
    else:
        if st.button("Login"):
            login_dialog()

        if st.button("Sign Up"):
            signup_dialog()

        if st.button("Create New Chat"):
            st.session_state.chat_id = None
            st.session_state.messages = []
            st.session_state.welcomed = False
            st.session_state.network_selected = False
            st.query_params = {"jwt": st.session_state.jwt, "selected_network": "n"}
            st.rerun()

st.write("### Selecciona una red bayesiana")
if 'network_selected' not in st.session_state:
    st.session_state.network_selected = False

if not st.session_state.network_selected:
    col1, col2 = st.columns(2)

    if col1.button("Ruidos"):
        st.session_state.selected_network = "r"
        st.session_state.messages = []
        st.session_state.responses = []
        st.session_state.question_index = 0
        st.session_state.welcomed = False
        st.session_state.network_selected = True
        st.query_params = {"jwt": st.session_state.jwt, "selected_network": "r"}
        st.rerun()

    if col2.button("Eléctrico"):
        st.session_state.selected_network = "e"
        st.session_state.messages = []
        st.session_state.responses = []
        st.session_state.question_index = 0
        st.session_state.welcomed = False
        st.session_state.network_selected = True
        st.query_params = {"jwt": st.session_state.jwt, "selected_network": "e"}
        st.rerun()
else:
    st.write(f"Has seleccionado la red: {'Ruidos' if st.session_state.selected_network == 'r' else 'Eléctrico'}")

if st.session_state.selected_network is None:
    st.session_state.messages = []

# Lista de preguntas según la red seleccionada
if st.session_state.selected_network == "r":
    questions = [
        "¿Escuchas un ruido de traqueteo al encender o mientras conduces? (s/n)",
        "¿El ruido de traqueteo solo ocurre mientras el vehículo está en movimiento? (s/n)",
        "¿Sientes como si hubiera una bomba de tiempo debajo del asiento? (s/n)",
        "¿Escuchas un ruido al cambiar a punto muerto? (s/n)",
        "¿El vehículo emite un ruido al cambiar a reversa? (s/n)",
        "¿Notas r al pasar sobre baches o desniveles? (s/n)",
        "¿El vehículo presenta golpes o caídas durante los cambios de marcha? (s/n)",
        "¿Escuchas r o golpes al girar el volante? (s/n)",
        "¿Has cambiado recientemente los neumáticos? (s/n)",
        "¿Has retirado los tapacubos de las ruedas? (s/n)",
        "¿Has inspeccionado las huellas de los neumáticos y encontrado algo fuera de lo normal? (s/n)",
        "¿Escuchas un ruido constante a baja velocidad? (s/n)",
        "¿Notas r extraños al arrancar el vehículo en frío? (s/n)",
        "¿Los limpiaparabrisas hacen ruido o detectas sonidos externos con el radio apagado? (s/n)"
    ]
elif st.session_state.selected_network == "e":
    questions = [
        "¿La batería se descarga rápidamente? (s/n)",
        "¿El alternador emite r o parece no cargar correctamente? (s/n)",
        "¿Hay algún problema con el cableado, como conexiones sueltas o quemadas? (s/n)",
        "¿Hay algún fusible fundido? (s/n)",
        "¿Las luces delanteras o del tablero tienen problemas, como parpadeos? (s/n)",
        "¿El vehículo presenta problemas para encender? (s/n)",
        "¿Hay problemas eléctricos generales, como dispositivos que no funcionan? (s/n)"
    ]

else:
    st.write("Por favor selecciona una red bayesiana para continuar.")
    st.stop()

if(st.session_state.selected_network == None):
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Show welcome message and first question if not welcomed yet
if not st.session_state.welcomed and st.session_state.selected_network:
    if st.session_state.chat_id is None:
        st.session_state.chat_id = str(uuid.uuid4())
    welcome_message = get_welcome_message(st.session_state.selected_network)
    st.session_state.messages.append({"role": "assistant", "content": f"Chat ID: {st.session_state.chat_id}"})
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})
    st.session_state.messages.append({"role": "assistant", "content": questions[0]})
    st.session_state.welcomed = True
    st.rerun()

# Manejo del flujo de preguntas
if prompt := st.chat_input("Responde a la pregunta..."):
    if st.session_state.chat_id is None:
        st.session_state.chat_id = str(uuid.uuid4())
    
    # Guardar respuesta del usuario
    st.session_state.responses.append(prompt.lower())
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Mostrar pregunta siguiente
    st.session_state.question_index += 1
    if st.session_state.question_index < len(questions):
        next_question = questions[st.session_state.question_index]
        st.session_state.messages.append(
            {"role": "assistant", "content": next_question})
    else:
        # Obtener diagnóstico de la red seleccionada
        response = get_bayesian_response(st.session_state.responses)
        st.session_state.messages.append(
            {"role": "assistant", "content": response})
        
        # Reiniciar para la siguiente sesión
        st.session_state.question_index = 0
        st.session_state.responses = []
        st.session_state.welcomed = False
        st.session_state.network_selected = False

    st.rerun()

if st.session_state.user_id and st.session_state.chat_id:
    save_chat_to_db(st.session_state.user_id, st.session_state.chat_id, st.session_state.messages)