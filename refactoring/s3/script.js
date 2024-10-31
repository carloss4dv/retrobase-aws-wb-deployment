const API_BASE_URL = "https://<API_GATEWAY_ID>.execute-api.<region>.amazonaws.com/prod"; // Cambia API_GATEWAY_ID y region

async function fetchAllPrograms() {
    const errorMessage = document.getElementById("errorMessage");
    errorMessage.textContent = ""; // Limpiar mensaje de error
    try {
        const response = await fetch(API_BASE_URL + '/get-all-programs', {
            method: "GET",
            headers: { "Content-Type": "application/json" },
        });

        if (response.status === 404) {
            errorMessage.textContent = "No se encontró ningún dato en el servidor.";
            return;
        } else if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        errorMessage.textContent = `Error al conectar con el servidor: ${error.message}`;
        console.error("Error:", error);
    }
}

async function searchByName() {
    const name = document.getElementById("name").value.trim();
    const errorMessage = document.getElementById("errorMessage");
    errorMessage.textContent = ""; // Limpiar mensaje de error
    if (name === "") {
        errorMessage.textContent = "Por favor, introduzca un nombre para buscar.";
        return;
    }
    await fetchData('/name', {program_name: name });
}

async function searchByTape() {
    const tape = document.getElementById("tape").value.trim();
    const errorMessage = document.getElementById("errorMessage");
    errorMessage.textContent = ""; // Limpiar mensaje de error
    if (tape === "") {
        errorMessage.textContent = "Por favor, introduzca una cinta para buscar.";
        return;
    }
    await fetchData('/tape', {tape_name: tape });
}

async function fetchData(endpoint, bodyData) {
    const errorMessage = document.getElementById("errorMessage");
    errorMessage.textContent = ""; // Limpiar mensaje de error
    try {
        const response = await fetch(API_BASE_URL + endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(bodyData),
        });

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

