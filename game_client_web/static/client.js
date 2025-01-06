let socket = null;
let authToken = null;

const API_URL = 'http://localhost:8000';
const WS_URL = 'ws://localhost:8000';

// Utility functions
function showError(message, elementId = 'auth-status') {
    const statusElement = document.getElementById(elementId);
    statusElement.className = 'status error';
    statusElement.textContent = message;
}

function showSuccess(message, elementId = 'auth-status') {
    const statusElement = document.getElementById(elementId);
    statusElement.className = 'status success';
    statusElement.textContent = message;
}

function addMessage(message, isSystem = false) {
    const messagesDiv = document.getElementById('messages');
    const messageElement = document.createElement('div');
    messageElement.className = `message ${isSystem ? 'system' : ''}`;
    messageElement.textContent = message;
    messagesDiv.appendChild(messageElement);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Authentication functions
async function register() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!username || !password) {
        showError('Please enter both username and password');
        return;
    }

    try {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            showSuccess('Registration successful! You can now login.');
        } else {
            showError(data.detail || 'Registration failed');
        }
    } catch (error) {
        showError('Error during registration: ' + error.message);
    }
}

async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!username || !password) {
        showError('Please enter both username and password');
        return;
    }

    try {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch(`${API_URL}/token`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            authToken = data.access_token;
            showSuccess('Login successful!');
            document.getElementById('auth-panel').classList.add('hidden');
            document.getElementById('game-panel').classList.remove('hidden');
            connectWebSocket(username);
        } else {
            showError(data.detail || 'Login failed');
        }
    } catch (error) {
        showError('Error during login: ' + error.message);
    }
}

// WebSocket functions
function connectWebSocket(username) {
    socket = new WebSocket(`${WS_URL}/ws/${username}`);

    socket.onopen = () => {
        showSuccess('Connected to game server', 'game-status');
        addMessage('Connected to game server', true);
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.client_id && data.message) {
            addMessage(`${data.client_id}: ${JSON.stringify(data.message)}`);
        }
    };

    socket.onclose = () => {
        showError('Disconnected from game server', 'game-status');
        addMessage('Disconnected from game server', true);
    };

    socket.onerror = (error) => {
        showError('WebSocket error: ' + error.message, 'game-status');
    };
}

function sendMessage() {
    if (!socket || socket.readyState !== WebSocket.OPEN) {
        showError('Not connected to server', 'game-status');
        return;
    }

    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();

    if (message) {
        socket.send(JSON.stringify({
            type: 'message',
            content: message
        }));
        messageInput.value = '';
    }
}

// Event listeners
document.getElementById('message-input').addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Clear any existing messages
    document.getElementById('messages').innerHTML = '';
    document.getElementById('auth-status').innerHTML = '';
    document.getElementById('game-status').innerHTML = '';
});