// public/js/socket_client.js
document.addEventListener("DOMContentLoaded", () => {
    const socket = io(); // 클라이언트에서 서버로 Socket.IO 연결 생성
    const consoleOutput = document.getElementById('consoleOutput');

    // 서버에서 보낸 'consoleMessage' 이벤트를 수신
    socket.on('consoleMessage', (msg) => {
        // 새로운 메시지를 div에 추가
        const messageElement = document.createElement('div');
        messageElement.textContent = msg;
        consoleOutput.appendChild(messageElement);

        // 자동으로 스크롤을 가장 아래로 이동
        consoleOutput.scrollTop = consoleOutput.scrollHeight;
    });
});
