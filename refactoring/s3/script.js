const API_BASE_URL = "https://iudjdh18y8.execute-api.us-east-1.amazonaws.com/prod"; // Cambia API_GATEWAY_ID y region

async function searchByName() {
    const name = document.getElementById("name").value.trim();
    const errorMessage = document.getElementById("errorMessage");
    errorMessage.textContent = ""; // Limpiar mensaje de error
    if (name === "") {
        errorMessage.textContent = "Por favor, introduzca un nombre para buscar.";
        return;
    }
    await fetchData(API_BASE_URL + '/name', { name: name }, "POST");
}

async function getAllPrograms() {
    const errorMessage = document.getElementById("errorMessage");
    errorMessage.textContent = ""; // Limpiar mensaje de error
    await fetchData(API_BASE_URL + '/get-all-programs', {}, "GET");
}

async function searchByTape() {
    const tape = document.getElementById("tape").value.trim();
    const errorMessage = document.getElementById("errorMessage");
    errorMessage.textContent = ""; // Limpiar mensaje de error
    if (tape === "") {
        errorMessage.textContent = "Por favor, introduzca una cinta para buscar.";
        return;
    }
    
    // Crear la URL con el parámetro de consulta
    // Hacer la solicitud GET
    await fetchData(API_BASE_URL+'/tape',{tape: tape}, "POST"); // No se necesita cuerpo en GET
}

async function fetchData(endpoint, bodyData, type) {
    const errorMessage = document.getElementById("errorMessage");
    errorMessage.textContent = ""; // Limpiar mensaje de error

    const fetchOptions = {
        method: type,
        headers: { 
            "Content-Type": "application/json",
        },
    };

    // Solo añadir el cuerpo si es una solicitud POST
    if (type === "POST") {
        fetchOptions.body = JSON.stringify(bodyData);
    }

    console.log("Enviando petición a:", endpoint, "con datos:", fetchOptions);

    try {
        const response = await fetch(endpoint, fetchOptions);

        if (response.status === 404) {
            errorMessage.textContent = "No se encontró ningún dato en el servidor.";
            return;
        } else if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const data = await response.json();
        if (data.error) {
            errorMessage.textContent = `Error en el servidor: ${data.error}`;
        } else {
            displayResults(data);
        }
    } catch (error) {
        errorMessage.textContent = `Error al conectar con el servidor: ${error.message}`;
        console.error("Error:", error);
    }
}

function displayResults(data) {
    const tbody = document.getElementById("resultsBody");
    const numReg = document.getElementById("numReg");
    tbody.innerHTML = ""; // Limpiar resultados anteriores
    numReg.textContent = 0; // Resetear el contador

    if (data.data && data.data.length > 0) {
        data.data.forEach(item => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${item.Number}</td>
                <td>${item.Name}</td>
                <td>${item.Type}</td>
                <td>${item.Tape}</td>
            `;
            tbody.appendChild(row);
        });
        numReg.textContent = data.data.length;
    } else {
        numReg.textContent = 0;
        const errorMessage = document.getElementById("errorMessage");
        errorMessage.textContent = "No se encontraron resultados para la búsqueda.";
    }
}
