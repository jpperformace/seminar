from enum import Enum

class ChatState(str, Enum):
    WELCOME = "Welcome"
    GET_CONTEXT_INFO = "Get Context Info"
    CREATE_REPORT = "Create Report"
    FOLLOW_UP = "Follow-Up"

class Phasen(Enum):
    ORGANIZING = 'Organisieren'
    UNDERSTANDING = 'Verstehen'
    DESIGNING = 'Gestalten'
    EVALUATION = 'Bewerten'

##################### CONTEXT

response_options_UX_experience = ['Einsteiger – Erste Berührungspunkte, keine oder sehr geringe praktische Erfahrung',
                                  'Grundkenntnisse – Einzelne UX-Methoden bekannt, punktuell angewendet',
                                  'Fortgeschritten – Regelmäßige Anwendung nutzerzentrierter Methoden im Projektkontext',
                                  'Erfahren – Systematische Integration in Prozesse, klare Zuständigkeiten',
                                  'Sehr erfahren – Strategisch verankert, teamübergreifend gelebt, kontinuierliche Optimierung']

response_options_expert = ['True', 'False']

response_options_company_size = ['Startup (wenige Mitarbeitende, meist unter 20, stark wachstumsorientiert)',
                                 'Kleine Unternehmen (bis ca. 50 Mitarbeitende)',
                                 'mittlere / mittelständische Unternehmen (ca. 50–500)',
                                 'Große Unternehmen (mehr als 500)',
                                 'Konzern (mehrere tausend Mitarbeitende, oft international tätig)']


##################### RAG INPUT

def get_no_expert_condition() -> str:
    return f"Es gibt keine UX-Experten im Unternehmen. Wähle nur Methoden aus die keinen benötigen."

def get_method_condition(response:str) -> str:
    return f"Gib keine Methoden zurück die bereits in der Antwort enthalten sind: {response}. "

def get_method_search_string(phase: str) -> str:
    return f"Methoden Informationen Phase {phase}"

def get_method_user_input(phase: str) -> str:
    return f"Welche Methoden gibt es in der Phase {phase}?"

def get_ai_tool_condition() -> str:
    return "Gib nur KI-Tools zurück. Dabei soll der Name des KI-Tools enthalten sein."

def get_ai_tool_search_query(phase: str) -> str:
    return f"Tool-Name Prozessphase {phase} mit Kurzbeschreibung"

def get_ai_tool_user_input(phase: str) -> str:
    return f"Gib mir KI-Tools mit Kurzbeschreibung zurück, die man in der Phase {phase} anwenden kann?"
