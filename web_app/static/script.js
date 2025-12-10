document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatArea = document.getElementById('chat-area');
    const sendBtn = document.querySelector('.send-btn');

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message
        appendMessage(message, 'user');
        userInput.value = '';
        userInput.disabled = true;
        sendBtn.disabled = true;

        // Add typing indicator
        const loadingId = showTypingIndicator();
        scrollToBottom();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            });

            const data = await response.json();
            
            // Remove typing indicator
            removeTypingIndicator(loadingId);

            if (response.ok) {
                appendMessage(data.response, 'agent');
            } else {
                appendMessage('Sorry, I encountered an error. Please try again.', 'agent');
                console.error('Error:', data.error);
            }
        } catch (error) {
            removeTypingIndicator(loadingId);
            appendMessage('Sorry, network error occurred.', 'agent');
            console.error('Error:', error);
        } finally {
            userInput.disabled = false;
            sendBtn.disabled = false;
            userInput.focus();
            scrollToBottom();
        }
    });

    function appendMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        contentDiv.textContent = text; // Securely set text content
        
        const timeDiv = document.createElement('div');
        timeDiv.classList.add('message-time');
        timeDiv.textContent = 'Just now';
        
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);
        
        chatArea.appendChild(messageDiv);
        scrollToBottom();
    }

    function showTypingIndicator() {
        const id = 'typing-' + Date.now();
        const indicatorDiv = document.createElement('div');
        indicatorDiv.id = id;
        indicatorDiv.classList.add('typing-indicator');
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.classList.add('typing-dot');
            indicatorDiv.appendChild(dot);
        }
        
        chatArea.appendChild(indicatorDiv);
        return id;
    }

    function removeTypingIndicator(id) {
        const element = document.getElementById(id);
        if (element) {
            element.remove();
        }
    }

    function scrollToBottom() {
        chatArea.scrollTop = chatArea.scrollHeight;
    }
});


