from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import json
import time
from datetime import datetime
import threading
from queue import Queue
import uuid

# Import your existing modules
from get_links import get_links
from scrape import scrape_links, initialize_logs
from cleaning import combine_logs
from llm import call_gemini, context_combine_prompt

app = Flask(__name__)
CORS(app)

# Store active processing tasks
active_tasks = {}
task_queue = Queue()

class ResearchTask:
    def __init__(self, task_id, topic, response_style="Comprehensive", include_sources=True):
        self.task_id = task_id
        self.topic = topic
        self.response_style = response_style
        self.include_sources = include_sources
        self.status = "initializing"
        self.progress = 0
        self.current_step = ""
        self.start_time = time.time()
        self.result = None
        self.error = None
        self.metadata = {
            "sources_count": 0,
            "tokens_used": 0,
            "processing_time": 0
        }

def process_research_task(task):
    """Process a research task in the background"""
    try:
        active_tasks[task.task_id] = task
        
        # Step 1: Get links
        task.status = "searching"
        task.current_step = "Searching web sources"
        task.progress = 10
        
        links = get_links(task.topic)
        task.metadata["sources_count"] = len(links)
        task.progress = 25
        
        # Step 2: Scrape content
        task.status = "scraping"
        task.current_step = "Scraping content"
        
        log_folder = initialize_logs(task.topic)
        scrape_links(links, save_logs=True, log_folder=log_folder)
        task.progress = 50
        
        # Step 3: Process data
        task.status = "processing"
        task.current_step = "Processing data"
        
        context_from_logs = combine_logs(log_folder)
        task.progress = 75
        
        # Step 4: Generate insights
        task.status = "generating"
        task.current_step = "Generating insights"
        
        if context_from_logs:
            final_prompt = context_combine_prompt(
                context_from_logs, 
                task.topic, 
                task.response_style, 
                task.include_sources
            )
            
            # Estimate tokens (rough calculation)
            task.metadata["tokens_used"] = len(final_prompt) // 4
            
            answer = call_gemini(final_prompt)
            task.result = answer
            task.progress = 100
            task.status = "completed"
        else:
            task.error = "No information found for this topic"
            task.status = "error"
            
    except Exception as e:
        task.error = str(e)
        task.status = "error"
        print(f"Error processing task {task.task_id}: {e}")
    
    finally:
        task.metadata["processing_time"] = time.time() - task.start_time

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/style.css')
def serve_css():
    """Serve CSS file"""
    response = send_from_directory('.', 'style.css', mimetype='text/css')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/script.js')
def serve_js():
    """Serve JavaScript file"""
    return send_from_directory('.', 'script.js', mimetype='application/javascript')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

@app.route('/api/research', methods=['POST'])
def start_research():
    """Start a new research task"""
    try:
        data = request.get_json()
        
        if not data or 'topic' not in data:
            return jsonify({'error': 'Topic is required'}), 400
        
        topic = data['topic'].strip()
        if not topic:
            return jsonify({'error': 'Topic cannot be empty'}), 400
        
        response_style = data.get('response_style', 'Comprehensive')
        include_sources = data.get('include_sources', True)
        
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        # Create research task
        task = ResearchTask(task_id, topic, response_style, include_sources)
        
        # Start processing in background thread
        thread = threading.Thread(target=process_research_task, args=(task,))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'task_id': task_id,
            'status': 'started',
            'message': 'Research task started successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/research/<task_id>/status', methods=['GET'])
def get_research_status(task_id):
    """Get the status of a research task"""
    try:
        if task_id not in active_tasks:
            return jsonify({'error': 'Task not found'}), 404
        
        task = active_tasks[task_id]
        
        response = {
            'task_id': task_id,
            'status': task.status,
            'progress': task.progress,
            'current_step': task.current_step,
            'metadata': task.metadata
        }
        
        if task.status == 'completed':
            response['result'] = task.result
        elif task.status == 'error':
            response['error'] = task.error
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/research/<task_id>/result', methods=['GET'])
def get_research_result(task_id):
    """Get the final result of a research task"""
    try:
        if task_id not in active_tasks:
            return jsonify({'error': 'Task not found'}), 404
        
        task = active_tasks[task_id]
        
        if task.status != 'completed':
            return jsonify({
                'error': 'Task not completed yet',
                'status': task.status,
                'progress': task.progress
            }), 202
        
        return jsonify({
            'task_id': task_id,
            'result': task.result,
            'metadata': task.metadata,
            'topic': task.topic,
            'response_style': task.response_style,
            'include_sources': task.include_sources
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'active_tasks': len(active_tasks)
    })

@app.route('/api/tasks', methods=['GET'])
def list_tasks():
    """List all active tasks (for debugging)"""
    tasks_info = []
    for task_id, task in active_tasks.items():
        tasks_info.append({
            'task_id': task_id,
            'topic': task.topic,
            'status': task.status,
            'progress': task.progress,
            'start_time': task.start_time
        })
    
    return jsonify({
        'active_tasks': len(active_tasks),
        'tasks': tasks_info
    })

# Cleanup old tasks periodically
def cleanup_old_tasks():
    """Remove completed tasks older than 1 hour"""
    current_time = time.time()
    tasks_to_remove = []
    
    for task_id, task in active_tasks.items():
        # Remove tasks older than 1 hour
        if current_time - task.start_time > 3600:
            tasks_to_remove.append(task_id)
    
    for task_id in tasks_to_remove:
        del active_tasks[task_id]
    
    # Schedule next cleanup
    threading.Timer(300, cleanup_old_tasks).start()  # Run every 5 minutes

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Start cleanup timer
    cleanup_old_tasks()
    
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Move index.html to templates directory for Flask
    if os.path.exists('index.html') and not os.path.exists('templates/index.html'):
        import shutil
        shutil.move('index.html', 'templates/index.html')
    
    print("🚀 Professor AI Research Assistant Server Starting...")
    print("📡 Server will be available at: http://localhost:5000")
    print("🔧 API endpoints:")
    print("   POST /api/research - Start new research")
    print("   GET  /api/research/<task_id>/status - Get task status")
    print("   GET  /api/research/<task_id>/result - Get task result")
    print("   GET  /api/health - Health check")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
