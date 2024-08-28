// public/js/socket_client.js
const socket = io();

// Listen for consoleMessage events from the server
socket.on('consoleMessage', (message) => {
    const consoleOutput = document.getElementById('consoleOutput');
    consoleOutput.innerHTML += message + '<br>';
    consoleOutput.scrollTop = consoleOutput.scrollHeight; // Auto-scroll
});
