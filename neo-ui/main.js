const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const chatContainer = document.getElementById('chatContainer');
const sendBtn = document.getElementById('sendBtn');

const pdfUpload = document.getElementById('pdfUpload');
const uploadStatusText = document.getElementById('uploadStatusText');
const uploadBtn = document.getElementById('uploadBtn');

const sourcesList = document.getElementById('sourcesList');
const refreshSourcesBtn = document.getElementById('refreshSourcesBtn');

const neuralVisualizerCard = document.getElementById('neuralVisualizerCard');
const neuralCanvas = document.getElementById('neuralCanvas');
const neuralMetricText = document.getElementById('neuralMetricText');

const IS_LOCAL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const BASE_URL = IS_LOCAL ? 'http://localhost:5000' : 'https://stale-flies-stare.loca.lt';
const API_URL = `${BASE_URL}/chat`;


/* ==========================================================================
   Structured Multi-Layer Artificial Neural Network (ANN) Visualizer
   ========================================================================== */
class LayeredNeuralNetwork {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.layers = [];
        this.pulses = [];
        this.animId = null;
        this.isRunning = false;
        this.resize();
    }

    resize() {
        if (!this.canvas) return;
        this.canvas.width = this.canvas.offsetWidth || 700;
        this.canvas.height = this.canvas.offsetHeight || 210;
        this.initNetwork();
    }

    initNetwork() {
        this.layers = [];
        const layerCounts = [5, 7, 9, 7, 5]; // 5-layer ANN architecture
        const layerColors = ['#00f0ff', '#2563eb', '#10b981', '#8b5cf6', '#38bdf8'];
        
        const width = this.canvas.width;
        const height = this.canvas.height;
        const startX = width * 0.12;
        const endX = width * 0.88;
        const stepX = (endX - startX) / (layerCounts.length - 1);
        
        // Build node position structure
        for (let l = 0; l < layerCounts.length; l++) {
            const count = layerCounts[l];
            const color = layerColors[l];
            const x = startX + l * stepX;
            const nodes = [];
            
            const layerHeight = height * 0.75;
            const startY = (height - layerHeight) / 2 + 15;
            const stepY = layerHeight / (count - 1 || 1);
            
            for (let i = 0; i < count; i++) {
                nodes.push({
                    x: x,
                    y: startY + i * stepY,
                    color: color,
                    pulse: Math.random() * Math.PI * 2,
                    glow: 0
                });
            }
            this.layers.push(nodes);
        }
        
        this.pulses = [];
    }

    spawnPulse() {
        if (this.layers.length < 2) return;
        // Pick a random layer (0 to 3) and a random node in layer L and target node in L+1
        const l = Math.floor(Math.random() * (this.layers.length - 1));
        const srcIdx = Math.floor(Math.random() * this.layers[l].length);
        const tgtIdx = Math.floor(Math.random() * this.layers[l + 1].length);
        
        this.pulses.push({
            layer: l,
            src: this.layers[l][srcIdx],
            tgt: this.layers[l + 1][tgtIdx],
            progress: 0,
            speed: 0.02 + Math.random() * 0.02,
            color: this.layers[l][srcIdx].color
        });
    }

    start() {
        this.resize();
        this.isRunning = true;
        this.animate();
    }

    stop() {
        this.isRunning = false;
        if (this.animId) {
            cancelAnimationFrame(this.animId);
        }
    }

    animate() {
        if (!this.isRunning) return;

        // Dark background
        this.ctx.fillStyle = '#020617';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // Render Title "Artificial Neural Network" at top center
        this.ctx.font = '600 16px Inter, sans-serif';
        this.ctx.fillStyle = '#38bdf8';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('Artificial Neural Network', this.canvas.width / 2, 22);

        // Spawn new pulses periodically
        if (Math.random() < 0.35) {
            this.spawnPulse();
        }

        // Draw Curved Bezier Synaptic Connections between adjacent layers
        const centerX = this.canvas.width / 2;
        for (let l = 0; l < this.layers.length - 1; l++) {
            const currentLayer = this.layers[l];
            const nextLayer = this.layers[l + 1];

            for (let u of currentLayer) {
                for (let v of nextLayer) {
                    this.ctx.beginPath();
                    this.ctx.moveTo(u.x, u.y);
                    
                    // Curve control point bows outward away from center
                    const midX = (u.x + v.x) / 2;
                    const curveOffset = (midX - centerX) * 0.25;
                    const cpY = (u.y + v.y) / 2;
                    
                    this.ctx.quadraticCurveTo(midX + curveOffset, cpY, v.x, v.y);
                    
                    // Gradient stroke
                    const grad = this.ctx.createLinearGradient(u.x, u.y, v.x, v.y);
                    grad.addColorStop(0, `${u.color}33`);
                    grad.addColorStop(1, `${v.color}33`);
                    
                    this.ctx.strokeStyle = grad;
                    this.ctx.lineWidth = 0.8;
                    this.ctx.stroke();
                }
            }
        }

        // Update & Draw Pulses
        for (let i = this.pulses.length - 1; i >= 0; i--) {
            const p = this.pulses[i];
            p.progress += p.speed;

            if (p.progress >= 1) {
                p.tgt.glow = 1.0; // Trigger glow on destination node
                this.pulses.splice(i, 1);
                continue;
            }

            const midX = (p.src.x + p.tgt.x) / 2;
            const curveOffset = (midX - centerX) * 0.25;
            const cpY = (p.src.y + p.tgt.y) / 2;

            // Bezier position at t = progress
            const t = p.progress;
            const px = (1 - t) * (1 - t) * p.src.x + 2 * (1 - t) * t * (midX + curveOffset) + t * t * p.tgt.x;
            const py = (1 - t) * (1 - t) * p.src.y + 2 * (1 - t) * t * cpY + t * t * p.tgt.y;

            // Draw signal pulse
            this.ctx.fillStyle = p.color;
            this.ctx.shadowColor = p.color;
            this.ctx.shadowBlur = 10;
            this.ctx.beginPath();
            this.ctx.arc(px, py, 3.5, 0, Math.PI * 2);
            this.ctx.fill();
            this.ctx.shadowBlur = 0;
        }

        // Draw Nodes
        for (let l = 0; l < this.layers.length; l++) {
            for (let node of this.layers[l]) {
                node.pulse += 0.05;
                if (node.glow > 0) node.glow -= 0.04;

                const baseRadius = 4.5;
                const glowRadius = baseRadius + Math.sin(node.pulse) * 1 + (node.glow * 3);

                // Outer glowing halo
                this.ctx.fillStyle = node.color;
                this.ctx.shadowColor = node.color;
                this.ctx.shadowBlur = 12 + (node.glow * 10);
                
                this.ctx.beginPath();
                this.ctx.arc(node.x, node.y, Math.max(2, glowRadius), 0, Math.PI * 2);
                this.ctx.fill();
                this.ctx.shadowBlur = 0;

                // Inner core
                this.ctx.fillStyle = '#ffffff';
                this.ctx.beginPath();
                this.ctx.arc(node.x, node.y, 2, 0, Math.PI * 2);
                this.ctx.fill();
            }
        }

        // Overlay random vector distance metric values
        if (Math.random() < 0.1) {
            const metrics = [
                `Layer_0 (Input): Dim(384) Vector Query`,
                `Layer_2 (Latent): Cosine Similarity = 0.942`,
                `Layer_4 (Output): Top 3 Chunks Retrieved`,
                `ChromaDB Vector Distance: 0.118 (MinLM)`
            ];
            const randMetric = metrics[Math.floor(Math.random() * metrics.length)];
            if (neuralMetricText) {
                neuralMetricText.textContent = randMetric;
            }
        }

        this.animId = requestAnimationFrame(() => this.animate());
    }
}

const visualizer = new LayeredNeuralNetwork(neuralCanvas);

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

const toggleVisualizerBtn = document.getElementById('toggleVisualizerBtn');
const closeVisualizerBtn = document.getElementById('closeVisualizerBtn');

if (toggleVisualizerBtn) {
    toggleVisualizerBtn.addEventListener('click', () => {
        const isHidden = neuralVisualizerCard.classList.contains('hidden');
        if (isHidden) {
            neuralVisualizerCard.classList.remove('hidden');
            visualizer.start();
        } else {
            visualizer.stop();
            neuralVisualizerCard.classList.add('hidden');
        }
    });
}

if (closeVisualizerBtn) {
    closeVisualizerBtn.addEventListener('click', () => {
        visualizer.stop();
        neuralVisualizerCard.classList.add('hidden');
    });
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const question = userInput.value.trim();
    if (!question) return;

    addMessage(question, 'user');
    userInput.value = '';

    const loadingMsgText = 'Thinking...';
    const loadingMsg = addMessage(loadingMsgText, 'ai', true);
    
    sendBtn.disabled = true;
    sendBtn.classList.add('opacity-50', 'cursor-not-allowed');

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });

        const data = await response.json();
        chatContainer.removeChild(loadingMsg);

        if (response.ok) {
            addMessage(data.answer, 'ai', false, data.log_id);
        } else {
            addMessage(`Error: ${data.answer || data.error || 'Something went wrong.'}`, 'ai');
        }
    } catch (error) {
        if (chatContainer.contains(loadingMsg)) {
            chatContainer.removeChild(loadingMsg);
        }
        addMessage(`Connection error: Make sure app.py is running on port 5000.`, 'ai');
        console.error('Error fetching chat:', error);
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
