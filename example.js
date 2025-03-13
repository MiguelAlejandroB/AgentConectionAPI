const fetch = require('node-fetch');

// Primera solicitud: Login
async function fetchLogin() {
  const url = "https://apiauthmatrixtest.azurewebsites.net/api/v2/Login";
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      nickName: $vars.API_NICKNAME, // Campo esperado por el backend
      password: $vars.API_PASSWORD, // Campo esperado por el backend
    })
  };

  try {
    const response = await fetch(url, options);
    const result = await response.json();
    console.log("Respuesta de Login:", result);
    return result;
  } catch (error) {
    console.error("Error en fetchLogin:", error);
    return '';
  }
}

// Segunda solicitud: Token
async function fetchToken(token) {
  //const token = "Pruebas";
  const url = "http://127.0.0.1:8030/Token/";
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      Token: token, // Campo esperado por el backend
    })
  };

  try {
    const response = await fetch(url, options);
    const result = await response.text();
    console.log("Respuesta de Token:", result);
    return result;
  } catch (error) {
    console.error("Error en fetchToken:", error);
    return '';
  }
}



// Tercera solicitud: Enviar Token y JSON
async function fetchJSON(token, toolInput) {
    const url = "http://127.0.0.1:8030/JSON_API/";
    const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer Bearer ${token}`},
      body: JSON.stringify({
        
    "electronicDocumentOriginId": 0,
    "documentTypeId": 0,
    "subject": "",
    "priorityId": 0,
    "internal": 0,
    "documentNumber": "",
    "graphSingnature": "",
    "sender": {
      "identificationNumber": $identificationNumber ,
      "documentTypeId": $documentTypeId,
      "name": $name,
      "lastName": $lastName,
      "email": $email,
      "phone": $phone,
      "active": true,
      "fullName": "string",
      "address": $address || "string",
      "company": ""
    },
    "receivers": [],
    "receiverToCopy": [],
    "creator": "string",
    "documentBase64": "",
    "metaData": [],
    "attachment": []
   // Campo esperado por el backend
      })
    };
  
    try {
      const response = await fetch(url, options);
      const result = await response.text();
      console.log("Respuesta de JSON:", result);
      return result;
    } catch (error) {
      console.error("Error en fetchJSON:", error);
      return '';
    }
  }

// Ejecutar las funciones
(async () => {
  const loginResponse = await fetchLogin();
  console.log("Respuesta de login:", loginResponse);
  if (loginResponse) {
    const token = loginResponse.token;
    console.log("Token: ", token);
    const tokenResponse = await fetchToken(token);
    const JSONResponse = await fetchJSON(token);
  }
})();
