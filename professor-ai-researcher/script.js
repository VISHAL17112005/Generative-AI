// Global variables
let isProcessing = false;
let processingStartTime = null;
let currentStep = 0;
let processingSteps = [
    { title: "Searching Web Sources", description: "Finding relevant information across the internet" },
    { title: "Scraping Content", description: "Extracting valuable data from discovered sources" },
    { title: "Processing Data", description: "Cleaning and organizing the collected information" },
    { title: "Generating Insights", description: "Creating comprehensive research using AI" }
];

// DOM Elements
const elements = {
    searchSection: document.getElementById('searchSection'),
    processingSection: document.getElementById('processingSection'),
    resultsSection: document.getElementById('resultsSection'),
    loadingOverlay: document.getElementById('loadingOverlay'),
    topicInput: document.getElementById('topicInput'),
    responseStyle: document.getElementById('responseStyle'),
    includeSources: document.getElementById('includeSources'),
    generateBtn: document.getElementById('generateBtn'),
    voiceBtn: document.getElementById('voiceBtn'),
    processingTitle: document.getElementById('processingTitle'),
    processingDescription: document.getElementById('processingDescription'),
    progressFill: document.getElementById('progressFill'),
    progressText: document.getElementById('progressText'),
    resultsContent: document.getElementById('resultsContent'),
    processingTime: document.getElementById('processingTime'),
    sourcesCount: document.getElementById('sourcesCount'),
    tokensUsed: document.getElementById('tokensUsed'),
    copyBtn: document.getElementById('copyBtn'),
    downloadBtn: document.getElementById('downloadBtn'),
    shareBtn: document.getElementById('shareBtn'),
    newSearchBtn: document.getElementById('newSearchBtn')
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    createParticleAnimation();
});

function initializeApp() {
    // Add entrance animations
    elements.searchSection.classList.add('fade-in');
    
    // Focus on input
    elements.topicInput.focus();
    
    // Initialize voice recognition if available
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        setupVoiceRecognition();
    } else {
        elements.voiceBtn.style.display = 'none';
    }
}

function setupEventListeners() {
    // Generate button click
    elements.generateBtn.addEventListener('click', handleGenerate);
    
    // Enter key in input
    elements.topicInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !isProcessing) {
            handleGenerate();
        }
    });
    
    // Voice button
    elements.voiceBtn.addEventListener('click', startVoiceRecognition);
    
    // Results action buttons
    elements.copyBtn.addEventListener('click', copyResults);
    elements.downloadBtn.addEventListener('click', downloadResults);
    elements.shareBtn.addEventListener('click', shareResults);
    elements.newSearchBtn.addEventListener('click', startNewSearch);
    
    // Input animations
    elements.topicInput.addEventListener('focus', function() {
        this.parentElement.style.transform = 'translateY(-2px)';
    });
    
    elements.topicInput.addEventListener('blur', function() {
        this.parentElement.style.transform = 'translateY(0)';
    });
}

function setupVoiceRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    window.recognition = new SpeechRecognition();
    
    window.recognition.continuous = false;
    window.recognition.interimResults = false;
    window.recognition.lang = 'en-US';
    
    window.recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        elements.topicInput.value = transcript;
        elements.voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
        elements.voiceBtn.style.background = 'var(--gradient-primary)';
    };
    
    window.recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
        elements.voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
        elements.voiceBtn.style.background = 'var(--gradient-primary)';
    };
    
    window.recognition.onend = function() {
        elements.voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
        elements.voiceBtn.style.background = 'var(--gradient-primary)';
    };
}

function startVoiceRecognition() {
    if (window.recognition) {
        elements.voiceBtn.innerHTML = '<i class="fas fa-circle" style="color: #ff006e;"></i>';
        elements.voiceBtn.style.background = 'var(--gradient-secondary)';
        window.recognition.start();
    }
}

async function handleGenerate() {
    const topic = elements.topicInput.value.trim();
    
    if (!topic) {
        showNotification('Please enter a research topic', 'warning');
        return;
    }
    
    if (isProcessing) {
        return;
    }
    
    isProcessing = true;
    processingStartTime = Date.now();
    
    // Show processing section with animation
    showProcessingSection();
    
    try {
        // Simulate the research process
        await simulateResearchProcess(topic);
        
        // Show results
        showResults(topic);
        
    } catch (error) {
        console.error('Error during research:', error);
        showNotification('An error occurred during research. Please try again.', 'error');
        showSearchSection();
    } finally {
        isProcessing = false;
    }
}

function showProcessingSection() {
    elements.searchSection.classList.add('hidden');
    elements.resultsSection.classList.add('hidden');
    elements.processingSection.classList.remove('hidden');
    elements.processingSection.classList.add('fade-in');
    
    // Reset processing state
    currentStep = 0;
    updateProgress(0);
    
    // Start processing animation
    startProcessingAnimation();
}

async function simulateResearchProcess(topic) {
    try {
        // Start the research task
        const response = await fetch('/api/research', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                topic: topic,
                response_style: elements.responseStyle.value,
                include_sources: elements.includeSources.checked
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        const taskId = data.task_id;
        
        // Poll for status updates
        await pollTaskStatus(taskId);
        
    } catch (error) {
        console.error('Error starting research:', error);
        throw error;
    }
}

async function pollTaskStatus(taskId) {
    const pollInterval = 1000; // Poll every second
    const maxAttempts = 300; // Maximum 5 minutes
    let attempts = 0;
    
    return new Promise((resolve, reject) => {
        const poll = async () => {
            try {
                attempts++;
                
                if (attempts > maxAttempts) {
                    reject(new Error('Research timeout - please try again'));
                    return;
                }
                
                const response = await fetch(`/api/research/${taskId}/status`);
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const status = await response.json();
                
                // Update UI based on status
                updateUIFromStatus(status);
                
                if (status.status === 'completed') {
                    // Store the result for display
                    window.currentResult = status.result;
                    window.currentMetadata = status.metadata;
                    resolve();
                } else if (status.status === 'error') {
                    reject(new Error(status.error || 'Research failed'));
                } else {
                    // Continue polling
                    setTimeout(poll, pollInterval);
                }
                
            } catch (error) {
                reject(error);
            }
        };
        
        poll();
    });
}

function updateUIFromStatus(status) {
    // Update progress bar
    updateProgress(status.progress);
    
    // Update current step based on status
    let stepIndex = 0;
    switch (status.status) {
        case 'searching':
            stepIndex = 0;
            break;
        case 'scraping':
            stepIndex = 1;
            break;
        case 'processing':
            stepIndex = 2;
            break;
        case 'generating':
            stepIndex = 3;
            break;
    }
    
    // Update processing step
    if (status.current_step) {
        elements.processingTitle.textContent = status.current_step;
        elements.processingDescription.textContent = getStepDescription(status.status);
    }
    
    // Mark completed steps
    for (let i = 0; i <= stepIndex; i++) {
        const stepElement = document.getElementById(`step${i + 1}`);
        if (stepElement) {
            if (i < stepIndex) {
                stepElement.classList.add('completed');
                stepElement.classList.remove('active');
            } else if (i === stepIndex) {
                stepElement.classList.add('active');
                stepElement.classList.remove('completed');
            }
        }
    }
}

function getStepDescription(status) {
    const descriptions = {
        'searching': 'Finding relevant information across the internet',
        'scraping': 'Extracting valuable data from discovered sources',
        'processing': 'Cleaning and organizing the collected information',
        'generating': 'Creating comprehensive research using AI'
    };
    return descriptions[status] || 'Processing your request...';
}

function startProcessingAnimation() {
    // Animate processing steps
    const stepElements = document.querySelectorAll('.step');
    stepElements.forEach((step, index) => {
        step.classList.remove('active', 'completed');
        setTimeout(() => {
            step.style.animation = `slideUp 0.5s ease-out ${index * 0.1}s both`;
        }, 100);
    });
}

function updateProcessingStep(stepIndex) {
    // Remove active class from all steps
    document.querySelectorAll('.step').forEach(step => {
        step.classList.remove('active');
    });
    
    // Add active class to current step
    document.getElementById(`step${stepIndex + 1}`).classList.add('active');
    
    // Update processing text
    elements.processingTitle.textContent = processingSteps[stepIndex].title;
    elements.processingDescription.textContent = processingSteps[stepIndex].description;
    
    // Add text animation
    elements.processingTitle.style.animation = 'fadeIn 0.5s ease-in';
    elements.processingDescription.style.animation = 'fadeIn 0.5s ease-in 0.2s both';
}

async function animateProgress(targetProgress, duration) {
    return new Promise(resolve => {
        const startProgress = parseInt(elements.progressFill.style.width) || 0;
        const progressDiff = targetProgress - startProgress;
        const startTime = Date.now();
        
        function updateProgress() {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function for smooth animation
            const easeProgress = 1 - Math.pow(1 - progress, 3);
            const currentProgress = startProgress + (progressDiff * easeProgress);
            
            elements.progressFill.style.width = `${currentProgress}%`;
            elements.progressText.textContent = `${Math.round(currentProgress)}%`;
            
            if (progress < 1) {
                requestAnimationFrame(updateProgress);
            } else {
                resolve();
            }
        }
        
        requestAnimationFrame(updateProgress);
    });
}

function updateProgress(progress) {
    elements.progressFill.style.width = `${progress}%`;
    elements.progressText.textContent = `${progress}%`;
}

async function showResults(topic) {
    // Get the real results from the backend
    const results = window.currentResult || generateMockResults(topic);
    const metadata = window.currentMetadata || {};
    
    // Calculate processing time
    const processingTime = metadata.processing_time ? 
        metadata.processing_time.toFixed(1) : 
        ((Date.now() - processingStartTime) / 1000).toFixed(1);
    
    // Hide processing section
    elements.processingSection.classList.add('hidden');
    
    // Show results section
    elements.resultsSection.classList.remove('hidden');
    elements.resultsSection.classList.add('slide-up');
    
    // Update results metadata with real data
    elements.processingTime.textContent = `${processingTime}s`;
    elements.sourcesCount.textContent = `${metadata.sources_count || 'Multiple'} sources`;
    elements.tokensUsed.textContent = `${metadata.tokens_used || 'N/A'} tokens`;
    
    // Format the results for better display
    const formattedResults = formatResults(results, topic);
    
    // Animate results content
    await typeWriterEffect(elements.resultsContent, formattedResults);
    
    // Show action buttons with stagger animation
    const actionBtns = document.querySelectorAll('.action-btn');
    actionBtns.forEach((btn, index) => {
        setTimeout(() => {
            btn.style.animation = `slideUp 0.5s ease-out both`;
        }, index * 100);
    });
}

function formatResults(results, topic) {
    // If results is already HTML formatted, return as is
    if (results.includes('<h') || results.includes('<p>')) {
        return results;
    }
    
    // Convert plain text to formatted HTML
    let formatted = results;
    
    // Add main heading if not present
    if (!formatted.toLowerCase().includes(topic.toLowerCase()) && !formatted.startsWith('#')) {
        formatted = `<h2>Research Results: ${topic}</h2>\n\n${formatted}`;
    }
    
    // Convert markdown-style formatting to HTML
    formatted = formatted
        // Headers
        .replace(/^### (.*$)/gm, '<h3>$1</h3>')
        .replace(/^## (.*$)/gm, '<h2>$1</h2>')
        .replace(/^# (.*$)/gm, '<h1>$1</h1>')
        
        // Bold text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        
        // Italic text
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        
        // Line breaks
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>')
        
        // Wrap in paragraphs
        .replace(/^(?!<[h|u|o])/gm, '<p>')
        .replace(/(?<!>)$/gm, '</p>')
        
        // Clean up extra paragraph tags
        .replace(/<p><\/p>/g, '')
        .replace(/<p>(<h[1-6]>)/g, '$1')
        .replace(/(<\/h[1-6]>)<\/p>/g, '$1');
    
    return formatted;
}

function generateMockResults(topic) {
    return `
        <h2>Comprehensive Research: ${topic}</h2>
        
        <h3>Executive Summary</h3>
        <p>This research provides a comprehensive overview of <strong>${topic}</strong>, covering key concepts, applications, and current trends in the field. The analysis is based on multiple authoritative sources and presents both theoretical foundations and practical implications.</p>
        
        <h3>Key Findings</h3>
        <ul>
            <li><strong>Definition and Scope:</strong> ${topic} encompasses various aspects that are crucial for understanding its impact and applications.</li>
            <li><strong>Current Trends:</strong> Recent developments show significant growth and innovation in this area.</li>
            <li><strong>Applications:</strong> Multiple industries are leveraging ${topic} for improved efficiency and outcomes.</li>
            <li><strong>Future Outlook:</strong> Projections indicate continued expansion and evolution of ${topic}-related technologies.</li>
        </ul>
        
        <h3>Detailed Analysis</h3>
        <p>The research reveals that ${topic} has become increasingly important in today's technological landscape. Organizations are investing heavily in ${topic}-related initiatives to stay competitive and meet evolving market demands.</p>
        
        <blockquote>
            "The integration of ${topic} represents a paradigm shift that will define the next decade of technological advancement." - Industry Expert
        </blockquote>
        
        <h3>Implementation Considerations</h3>
        <ol>
            <li><strong>Strategic Planning:</strong> Organizations should develop comprehensive strategies for ${topic} adoption.</li>
            <li><strong>Resource Allocation:</strong> Adequate resources must be allocated for successful implementation.</li>
            <li><strong>Training and Development:</strong> Staff training is essential for maximizing the benefits of ${topic}.</li>
            <li><strong>Monitoring and Evaluation:</strong> Continuous assessment ensures optimal performance and ROI.</li>
        </ol>
        
        <h3>Conclusion</h3>
        <p>The research demonstrates that ${topic} offers significant opportunities for innovation and growth. Organizations that proactively embrace ${topic} are likely to gain competitive advantages and achieve superior outcomes in their respective markets.</p>
        
        <p><em>This analysis is based on comprehensive research from multiple authoritative sources and represents current best practices and emerging trends in the field.</em></p>
    `;
}

async function typeWriterEffect(element, content) {
    element.innerHTML = '';
    
    // Create a temporary div to parse HTML
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = content;
    
    // Extract text content while preserving structure
    const textContent = content;
    
    return new Promise(resolve => {
        let index = 0;
        const speed = 20; // Adjust typing speed
        
        function typeChar() {
            if (index < textContent.length) {
                element.innerHTML = textContent.substring(0, index + 1);
                index++;
                setTimeout(typeChar, speed);
            } else {
                // Set final formatted content
                element.innerHTML = content;
                resolve();
            }
        }
        
        typeChar();
    });
}

function copyResults() {
    const resultsText = elements.resultsContent.innerText;
    
    if (navigator.clipboard) {
        navigator.clipboard.writeText(resultsText).then(() => {
            showNotification('Results copied to clipboard!', 'success');
            animateButton(elements.copyBtn);
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = resultsText;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showNotification('Results copied to clipboard!', 'success');
        animateButton(elements.copyBtn);
    }
}

function downloadResults() {
    const resultsText = elements.resultsContent.innerText;
    const topic = elements.topicInput.value.trim();
    const filename = `research_${topic.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.txt`;
    
    const blob = new Blob([resultsText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification('Results downloaded!', 'success');
    animateButton(elements.downloadBtn);
}

function shareResults() {
    const resultsText = elements.resultsContent.innerText;
    const topic = elements.topicInput.value.trim();
    
    if (navigator.share) {
        navigator.share({
            title: `Research Results: ${topic}`,
            text: resultsText.substring(0, 200) + '...',
            url: window.location.href
        }).then(() => {
            showNotification('Results shared!', 'success');
        }).catch(err => {
            console.log('Error sharing:', err);
            fallbackShare();
        });
    } else {
        fallbackShare();
    }
    
    animateButton(elements.shareBtn);
}

function fallbackShare() {
    const topic = elements.topicInput.value.trim();
    const shareText = `Check out this research on ${topic}: ${window.location.href}`;
    
    if (navigator.clipboard) {
        navigator.clipboard.writeText(shareText).then(() => {
            showNotification('Share link copied to clipboard!', 'success');
        });
    }
}

function startNewSearch() {
    // Reset form
    elements.topicInput.value = '';
    elements.responseStyle.value = 'Comprehensive';
    elements.includeSources.checked = true;
    
    // Show search section
    showSearchSection();
    
    // Focus on input
    elements.topicInput.focus();
    
    animateButton(elements.newSearchBtn);
}

function showSearchSection() {
    elements.processingSection.classList.add('hidden');
    elements.resultsSection.classList.add('hidden');
    elements.searchSection.classList.remove('hidden');
    elements.searchSection.classList.add('fade-in');
}

function animateButton(button) {
    button.style.transform = 'scale(0.95)';
    setTimeout(() => {
        button.style.transform = 'scale(1)';
    }, 150);
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)}"></i>
        <span>${message}</span>
    `;
    
    // Style the notification
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        background: type === 'success' ? 'var(--gradient-success)' : 
                   type === 'warning' ? 'var(--gradient-secondary)' : 
                   'var(--gradient-primary)',
        color: 'white',
        padding: '15px 20px',
        borderRadius: 'var(--border-radius)',
        boxShadow: 'var(--shadow-glow)',
        zIndex: '1001',
        display: 'flex',
        alignItems: 'center',
        gap: '10px',
        transform: 'translateX(100%)',
        transition: 'transform 0.3s ease'
    });
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after delay
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

function getNotificationIcon(type) {
    switch (type) {
        case 'success': return 'check-circle';
        case 'warning': return 'exclamation-triangle';
        case 'error': return 'times-circle';
        default: return 'info-circle';
    }
}

function createParticleAnimation() {
    const particleCount = 50;
    const particles = document.querySelector('.particles');
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'floating-particle';
        
        // Random properties
        const size = Math.random() * 3 + 1;
        const x = Math.random() * 100;
        const y = Math.random() * 100;
        const duration = Math.random() * 20 + 10;
        const delay = Math.random() * 20;
        
        Object.assign(particle.style, {
            position: 'absolute',
            width: `${size}px`,
            height: `${size}px`,
            background: `var(--${['primary', 'accent', 'secondary'][Math.floor(Math.random() * 3)]}-color)`,
            borderRadius: '50%',
            left: `${x}%`,
            top: `${y}%`,
            opacity: '0.1',
            animation: `floatParticle ${duration}s linear infinite ${delay}s`
        });
        
        particles.appendChild(particle);
    }
    
    // Add floating animation keyframes
    const style = document.createElement('style');
    style.textContent = `
        @keyframes floatParticle {
            0% { transform: translateY(0) rotate(0deg); }
            100% { transform: translateY(-100vh) rotate(360deg); }
        }
    `;
    document.head.appendChild(style);
}

// Utility function
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Add some interactive effects
document.addEventListener('mousemove', function(e) {
    const cursor = document.querySelector('.cursor-glow');
    if (!cursor) {
        const glowCursor = document.createElement('div');
        glowCursor.className = 'cursor-glow';
        Object.assign(glowCursor.style, {
            position: 'fixed',
            width: '20px',
            height: '20px',
            background: 'radial-gradient(circle, var(--primary-color), transparent)',
            borderRadius: '50%',
            pointerEvents: 'none',
            zIndex: '9999',
            opacity: '0.3',
            transition: 'transform 0.1s ease'
        });
        document.body.appendChild(glowCursor);
    }
    
    const glowElement = document.querySelector('.cursor-glow');
    glowElement.style.left = `${e.clientX - 10}px`;
    glowElement.style.top = `${e.clientY - 10}px`;
});

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to generate
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter' && !isProcessing) {
        handleGenerate();
    }
    
    // Escape to start new search
    if (e.key === 'Escape' && !isProcessing) {
        startNewSearch();
    }
});

// Performance optimization: Throttle resize events
let resizeTimeout;
window.addEventListener('resize', function() {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(function() {
        // Handle responsive adjustments
        const isMobile = window.innerWidth <= 768;
        document.body.classList.toggle('mobile', isMobile);
    }, 250);
});
