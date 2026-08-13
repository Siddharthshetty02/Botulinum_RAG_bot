const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const chatContainer = document.getElementById('chatContainer');
const sendBtn = document.getElementById('sendBtn');

const pdfUpload = document.getElementById('pdfUpload');
const uploadStatusText = document.getElementById('uploadStatusText');
const uploadBtn = document.getElementById('uploadBtn');

const sourcesList = document.getElementById('sourcesList');
const refreshSourcesBtn = document.getElementById('refreshSourcesBtn');

const IS_LOCAL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const BASE_URL = IS_LOCAL ? 'http://localhost:5000' : 'https://web-production-c48d4.up.railway.app';
const API_URL = `${BASE_URL}/chat`;

/* ==========================================================================
   Chat Messages & API Logic
   ========================================================================== */

function formatMarkdownText(text) {
    if (!text) return '';
    
    // Escape HTML characters
    let html = text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
        
    // Convert **bold** to <b class="font-bold text-white">
    html = html.replace(/\*\*(.*?)\*\*/g, '<b class="font-bold text-white">$1</b>');
    html = html.replace(/__(.*?)__/g, '<b class="font-bold text-white">$1</b>');
    
    // Convert `code` to highlighted span
    html = html.replace(/`([^`]+)`/g, '<code class="bg-slate-950 text-brand-lime px-1.5 py-0.5 rounded font-mono text-xs">$1</code>');
    
    // Preserve linebreaks
    html = html.replace(/\n/g, '<br>');
    return html;
}

function addMessage(text, sender, isLoading = false, logId = null) {
    const wrapper = document.createElement('div');
    wrapper.className = `flex items-start space-x-3 ${sender === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`;

    const avatar = document.createElement('div');
    if (sender === 'user') {
        avatar.className = 'w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-xs font-bold text-slate-300 flex-shrink-0';
        avatar.textContent = 'YOU';
    } else {
        avatar.className = 'w-8 h-8 rounded-lg bg-brand-lime/20 border border-brand-lime/40 flex items-center justify-center text-xs font-bold text-brand-lime flex-shrink-0';
        avatar.textContent = 'AI';
    }

    const bubble = document.createElement('div');
    bubble.className = sender === 'user'
        ? 'bg-brand-lime text-slate-950 font-medium rounded-2xl rounded-tr-none p-4 max-w-[85%] text-sm sm:text-base leading-relaxed shadow-md'
        : `bg-slate-800/90 border border-slate-700/70 rounded-2xl rounded-tl-none p-4 max-w-[85%] text-sm sm:text-base text-slate-200 leading-relaxed shadow-lg ${isLoading ? 'animate-pulse text-slate-400 italic' : ''}`;

    const textSpan = document.createElement('div');
    textSpan.className = 'markdown-content space-y-1';
    textSpan.innerHTML = formatMarkdownText(text);
    bubble.appendChild(textSpan);

    // Add Feedback Rating buttons if it's a completed AI response with a logId
    if (sender === 'ai' && !isLoading && logId) {
        const feedbackContainer = document.createElement('div');
        feedbackContainer.className = 'flex items-center space-x-2 mt-3 pt-2.5 border-t border-slate-700/50 text-xs text-slate-400';

        const label = document.createElement('span');
        label.textContent = 'Rate answer:';

        const upBtn = document.createElement('button');
        upBtn.className = 'hover:bg-slate-700 text-slate-300 font-bold px-2 py-1 rounded bg-slate-900 border border-slate-700 transition cursor-pointer';
        upBtn.textContent = '👍';

        const downBtn = document.createElement('button');
        downBtn.className = 'hover:bg-slate-700 text-slate-300 font-bold px-2 py-1 rounded bg-slate-900 border border-slate-700 transition cursor-pointer';
        downBtn.textContent = '👎';

        const statusSpan = document.createElement('span');
        statusSpan.className = 'text-brand-lime font-medium ml-1 hidden';

        async function sendFeedback(rating) {
            upBtn.disabled = true;
            downBtn.disabled = true;
            try {
                const res = await fetch(`${BASE_URL}/feedback`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ log_id: logId, rating })
                });
                if (res.ok) {
                    statusSpan.textContent = rating === 'up' ? 'Thanks! (👍 saved)' : 'Feedback logged (👎 saved)';
                    statusSpan.classList.remove('hidden');
                }
            } catch (err) {
                console.error('Feedback error:', err);
            }
        }

        upBtn.addEventListener('click', () => sendFeedback('up'));
        downBtn.addEventListener('click', () => sendFeedback('down'));

        feedbackContainer.appendChild(label);
        feedbackContainer.appendChild(upBtn);
        feedbackContainer.appendChild(downBtn);
        feedbackContainer.appendChild(statusSpan);
        bubble.appendChild(feedbackContainer);
    }

    wrapper.appendChild(avatar);
    wrapper.appendChild(bubble);
    chatContainer.appendChild(wrapper);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return wrapper;
}

function attachFeedbackContainer(bubble, logId) {
    if (!logId || bubble.querySelector('.feedback-box')) return;
    
    const feedbackContainer = document.createElement('div');
    feedbackContainer.className = 'feedback-box flex items-center space-x-2 mt-3 pt-2.5 border-t border-slate-700/50 text-xs text-slate-400';

    const label = document.createElement('span');
    label.textContent = 'Rate answer:';

    const upBtn = document.createElement('button');
    upBtn.className = 'hover:bg-slate-700 text-slate-300 font-bold px-2 py-1 rounded bg-slate-900 border border-slate-700 transition cursor-pointer';
    upBtn.textContent = '👍';

    const downBtn = document.createElement('button');
    downBtn.className = 'hover:bg-slate-700 text-slate-300 font-bold px-2 py-1 rounded bg-slate-900 border border-slate-700 transition cursor-pointer';
    downBtn.textContent = '👎';

    const statusSpan = document.createElement('span');
    statusSpan.className = 'text-brand-lime font-medium ml-1 hidden';

    async function sendFeedback(rating) {
        upBtn.disabled = true;
        downBtn.disabled = true;
        try {
            const res = await fetch(`${BASE_URL}/feedback`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ log_id: logId, rating })
            });
            if (res.ok) {
                statusSpan.textContent = rating === 'up' ? 'Thanks! (👍 saved)' : 'Feedback logged (👎 saved)';
                statusSpan.classList.remove('hidden');
            }
        } catch (err) {
            console.error('Feedback error:', err);
        }
    }

    upBtn.addEventListener('click', () => sendFeedback('up'));
    downBtn.addEventListener('click', () => sendFeedback('down'));

    feedbackContainer.appendChild(label);
    feedbackContainer.appendChild(upBtn);
    feedbackContainer.appendChild(downBtn);
    feedbackContainer.appendChild(statusSpan);
    bubble.appendChild(feedbackContainer);
}

function addStreamingMessage() {
    const wrapper = document.createElement('div');
    wrapper.className = 'flex items-start space-x-3';

    const avatar = document.createElement('div');
    avatar.className = 'w-8 h-8 rounded-lg bg-brand-lime/20 border border-brand-lime/40 flex items-center justify-center text-xs font-bold text-brand-lime flex-shrink-0';
    avatar.textContent = 'AI';

    const bubble = document.createElement('div');
    bubble.className = 'bg-slate-800/90 border border-slate-700/70 rounded-2xl rounded-tl-none p-4 max-w-[85%] text-sm sm:text-base text-slate-200 leading-relaxed shadow-lg';

    const textSpan = document.createElement('div');
    textSpan.className = 'markdown-content space-y-1';
    textSpan.innerHTML = '<span class="animate-pulse text-slate-400 italic">Thinking & typing...</span>';
    bubble.appendChild(textSpan);

    wrapper.appendChild(avatar);
    wrapper.appendChild(bubble);
    chatContainer.appendChild(wrapper);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    return {
        textSpan,
        bubble,
        setLogId: (logId) => attachFeedbackContainer(bubble, logId)
    };
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const question = userInput.value.trim();
    if (!question) return;

    addMessage(question, 'user');
    userInput.value = '';

    sendBtn.disabled = true;
    sendBtn.classList.add('opacity-50', 'cursor-not-allowed');

    const streamingObj = addStreamingMessage();
    let accumulatedText = '';
    let currentLogId = null;

    try {
        const response = await fetch(`${BASE_URL}/chat_stream`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });

        if (!response.ok) {
            streamingObj.textSpan.innerHTML = formatMarkdownText("❌ Error: Could not connect to LLM stream.");
            return;
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let buffer = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const parts = buffer.split('\n\n');
            buffer = parts.pop() || '';

            for (const part of parts) {
                const trimmed = part.trim();
                if (trimmed.startsWith('data: ')) {
                    try {
                        const payload = JSON.parse(trimmed.slice(6));
                        if (payload.token) {
                            accumulatedText += payload.token;
                            streamingObj.textSpan.innerHTML = formatMarkdownText(accumulatedText);
                            chatContainer.scrollTop = chatContainer.scrollHeight;
                        }
                        if (payload.log_id) {
                            currentLogId = payload.log_id;
                        }
                        if (payload.done && currentLogId) {
                            streamingObj.setLogId(currentLogId);
                        }
                    } catch (err) {
                        console.error('Error parsing SSE payload:', err);
                    }
                }
            }
        }

        if (!accumulatedText) {
            streamingObj.textSpan.innerHTML = formatMarkdownText("No response generated.");
        }
    } catch (error) {
        streamingObj.textSpan.innerHTML = formatMarkdownText("❌ Connection error: Make sure app.py is running on port 5000.");
        console.error('Error streaming chat:', error);
    } finally {
        sendBtn.disabled = false;
        sendBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    }
});

/* ==========================================================================
   Document Ingestion (Upload PDF)
   ========================================================================== */

pdfUpload.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    addMessage(`Uploading document: ${file.name}`, 'user');
    const loadingMsg = addMessage(`Converting "${file.name}" to Markdown & indexing into ChromaDB...`, 'ai', true);

    pdfUpload.value = '';

    const formData = new FormData();
    formData.append('file', file);

    const originalText = uploadStatusText.textContent;
    uploadStatusText.textContent = `Processing and indexing ${file.name}...`;
    uploadStatusText.style.color = '#a3e635';
    uploadBtn.style.pointerEvents = 'none';
    uploadBtn.style.opacity = '0.5';

    try {
        const response = await fetch(`${BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (chatContainer.contains(loadingMsg)) {
            chatContainer.removeChild(loadingMsg);
        }

        if (response.ok) {
            uploadStatusText.textContent = `✅ Success: ${file.name} added!`;
            addMessage(`✅ Successfully read, converted to Markdown, and indexed "${file.name}". You can now ask questions about it!`, 'ai');
            loadSources();
        } else {
            uploadStatusText.textContent = `❌ Error processing ${file.name}`;
            addMessage(`❌ Upload error: ${data.error || 'Failed to process PDF.'}`, 'ai');
        }
    } catch (error) {
        console.error('Error uploading file:', error);
        if (chatContainer.contains(loadingMsg)) {
            chatContainer.removeChild(loadingMsg);
        }
        uploadStatusText.textContent = `❌ Connection error while uploading.`;
        addMessage(`❌ Connection error: Could not reach Python backend.`, 'ai');
    } finally {
        uploadBtn.style.pointerEvents = 'auto';
        uploadBtn.style.opacity = '1';

        setTimeout(() => {
            uploadStatusText.textContent = originalText;
            uploadStatusText.style.color = '#94a3b8';
        }, 5000);
    }
});

/* ==========================================================================
   Knowledge Sources List & Delete Logic
   ========================================================================== */

async function loadSources() {
    try {
        const response = await fetch(`${BASE_URL}/sources`);
        const data = await response.json();

        sourcesList.innerHTML = '';
        if (!data.sources || data.sources.length === 0) {
            sourcesList.innerHTML = '<li class="text-xs text-slate-500 italic">No documents in Knowledge Base.</li>';
            return;
        }

        data.sources.forEach(source => {
            const li = document.createElement('li');
            li.className = 'flex items-center justify-between p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80 text-xs hover:border-slate-700 transition';

            const infoDiv = document.createElement('div');
            infoDiv.className = 'truncate pr-2';

            const title = document.createElement('div');
            title.className = 'font-semibold text-slate-200 truncate';
            title.textContent = source.name;

            const meta = document.createElement('div');
            meta.className = 'text-[10px] font-mono text-slate-400 truncate';
            meta.textContent = `${source.files.join(', ')} • ${source.size_kb} KB`;

            infoDiv.appendChild(title);
            infoDiv.appendChild(meta);

            const delBtn = document.createElement('button');
            delBtn.className = 'px-2 py-1 rounded-md bg-red-500/10 border border-red-500/20 text-red-400 hover:bg-red-500/20 text-[10px] font-semibold transition flex-shrink-0';
            delBtn.textContent = '🗑️ Delete';

            delBtn.addEventListener('click', () => deleteSource(source.name));

            li.appendChild(infoDiv);
            li.appendChild(delBtn);
            sourcesList.appendChild(li);
        });
    } catch (err) {
        console.error('Failed to load sources:', err);
        sourcesList.innerHTML = '<li class="text-xs text-red-400">Could not load sources from backend.</li>';
    }
}

async function deleteSource(sourceName) {
    addMessage(`Deleting source: ${sourceName}...`, 'user');
    const loadingMsg = addMessage(`Removing files for "${sourceName}" from disk and purging vector embeddings...`, 'ai', true);

    try {
        const response = await fetch(`${BASE_URL}/delete`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename: sourceName })
        });
        const data = await response.json();

        if (chatContainer.contains(loadingMsg)) {
            chatContainer.removeChild(loadingMsg);
        }

        if (response.ok) {
            addMessage(`🗑️ Successfully deleted "${sourceName}"! Disk space freed and vectors purged.`, 'ai');
            loadSources();
        } else {
            addMessage(`❌ Error deleting "${sourceName}": ${data.error || 'Failed to delete'}`, 'ai');
        }
    } catch (err) {
        if (chatContainer.contains(loadingMsg)) {
            chatContainer.removeChild(loadingMsg);
        }
        addMessage(`❌ Connection error: Could not reach backend server.`, 'ai');
    }
}

refreshSourcesBtn.addEventListener('click', loadSources);
loadSources();
