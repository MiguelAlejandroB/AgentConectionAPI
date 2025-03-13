from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, ValidationError
from datetime import datetime
from typing import List, Optional
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Definir los modelos Pydantic para los datos
class Sender(BaseModel):
    identificationNumber: str
    documentTypeId: str  # Acepta "CC" como string
    name: str
    lastName: str
    email: str
    phone: str
    active: bool
    fullName: str
    address: str
    company: Optional[str] = ""  # Se mantiene como opción vacía

class PQRS(BaseModel):
    electronicDocumentOriginId: int
    documentTypeId: int  # Acepta "CC" como string
    subject: Optional[str] = ""
    priorityId: int
    internal: int
    documentNumber: Optional[str] = ""
    graphSingnature: Optional[str] = ""
    sender: Sender
    receivers: List[str] = []
    receiverToCopy: List[str] = []
    creator: str
    documentBase64: Optional[str] = ""
    metaData: List[str] = []
    attachment: List[str] = []
class Token(BaseModel):
    Token: str

security = HTTPBearer()
current_token = None  # Almacena el último token recibido
# Crear la aplicación FastAPI

app = FastAPI(
    title="Mi API de prueba",  # Título personalizado
    version="1.0.0", docs_url="/documentacion" , # Versión semántica
    openapi_tags=[  # Define tus propios grupos (tags)
        {
            "name": "PQRS",
            "description": "Endpoints para gestión de PQRS"
        },
        {
            "name": "Autenticación",
            "description": "Manejo de tokens de acceso"
        }
    ]
)
# Agrupar endpoints bajo
v1 = APIRouter(prefix="/Pruebas")

async def obtener_token_actual(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return credentials.credentials

async def validar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    global current_token
    
    print(f"[DEBUG] Token recibido en header: {credentials.credentials}")  # Para debug
    print(f"[DEBUG] Token almacenado: {current_token}")  # Para debug
    
    if not current_token:
        raise HTTPException(401, "Token no configurado")
    
    if credentials.credentials != current_token:
        raise HTTPException(401, "Token inválido")
    
    return True

@app.post("/JSON_API/", tags=["PQRS"])
async def JSON_API(pqrs: PQRS, token: str = Depends(obtener_token_actual)):
    global current_token
    try:
                # Verifica autenticación
        if current_token is None:
            raise HTTPException(status_code=401, detail="Token no configurado")
        if token != current_token:
            print("Token invalido: ", token)
            print("Token real: ", current_token)
            raise HTTPException(status_code=401, detail="Token inválido")
        # Obtener la hora actual
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Imprimir en la consola el JSON recibido y la hora
        print(f"JSON recibido a las {current_time}:")
        print(pqrs.dict())

        # Validar que los campos requeridos estén presentes
        if not pqrs.sender.identificationNumber or not pqrs.sender.name:
            error_message = "Identificación o nombre del remitente faltante"
            print(f"Error de validación: {error_message}")
            raise HTTPException(status_code=400, detail=error_message)

        # Validaciones adicionales si es necesario
        if pqrs.sender.documentTypeId not in ["CC", "CE", "TI"]:
            error_message = "Tipo de documento inválido"
            print(f"Error de validación: {error_message}")
            raise HTTPException(status_code=400, detail=error_message)

        # Respuesta al cliente
        return {"message": "JSON recibido exitosamente", "timestamp": current_time}

    except ValidationError as ve:
        # Manejar errores de validación de Pydantic
        error_message = f"Error de validación: {ve}"
        print(error_message)
        raise HTTPException(status_code=422, detail=error_message)

    except HTTPException as he:
        # Manejar errores HTTP personalizados
        error_message = f"Error HTTP: {he.detail}"
        print(error_message)
        raise he

    except Exception as e:
        # Capturar cualquier otro tipo de error y mostrarlo en la consola
        error_message = f"Error inesperado: {e}"
        print(error_message)
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.post("/Token/", tags=["Autenticación"])
async def Token(token: Token):
    global current_token
    try:
        # Obtener la hora actual
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Imprimir en la consola el JSON recibido y la hora
        print(f"JSON recibido a las {current_time}:")
        print(token.dict())

        # Validar que los campos requeridos estén presentes
        if not token.Token:
            error_message = "Token faltante"
            print(f"Error de validación: {error_message}")
            raise HTTPException(status_code=400, detail=error_message)
        current_token = "Bearer "+ token.Token

        # Respuesta al cliente
        return {"message": "Token recibido exitosamente", "timestamp": current_time}

    except ValidationError as ve:
        # Manejar errores de validación de Pydantic
        error_message = f"Error de validación: {ve}"
        print(error_message)
        raise HTTPException(status_code=422, detail=error_message)

    except HTTPException as he:
        # Manejar errores HTTP personalizados
        error_message = f"Error HTTP: {he.detail}"
        print(error_message)
        raise he

    except Exception as e:
        # Capturar cualquier otro tipo de error y mostrarlo en la consola
        error_message = f"Error inesperado: {e}"
        print(error_message)
        raise HTTPException(status_code=500, detail="Error interno del servidor")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8030)
