#!/usr/bin/env python3
"""
Real File Integrity Monitor with Hash Verification
A production-ready security tool that actually calculates file hashes and detects changes.
"""

import hashlib
import os
import json
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class FileIntegrityMonitor:
    def __init__(self):
        self.baseline = {}
    
    def calculate_file_hash(self, file_path, algorithm='sha256'):
        hash_func = getattr(hashlib, algorithm)()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    
    def monitor_files(self, files, algorithm='sha256', mode='one-time'):
        results = {
            'summary': {'totalFiles': 0, 'validFiles': 0, 'modifiedFiles': 0, 'algorithm': algorithm.upper()},
            'files': [],
            'report': {'status': 'success', 'message': '', 'timestamp': datetime.now().isoformat()}
        }
        
        for file in files:
            try:
                file_hash = self.calculate_file_hash(file, algorithm)
                status = 'valid' if mode == 'one-time' else self._compare_with_baseline(file, file_hash)
                
                results['files'].append({
                    'name': os.path.basename(file),
                    'size': os.path.getsize(file),
                    'hash': file_hash,
                    'status': status,
                    'algorithm': algorithm.upper(),
                    'timestamp': datetime.now().isoformat()
                })
                
                results['summary']['totalFiles'] += 1
                if status == 'valid':
                    results['summary']['validFiles'] += 1
                else:
                    results['summary']['modifiedFiles'] += 1
                    
            except Exception as e:
                logger.error(f"Error processing {file}: {str(e)}")
        
        results['report']['message'] = f"Verified {results['summary']['totalFiles']} files"
        return results
    
    def _compare_with_baseline(self, file_path, current_hash):
        if file_path in self.baseline:
            return 'valid' if self.baseline[file_path] == current_hash else 'modified'
        self.baseline[file_path] = current_hash
        return 'valid'

monitor = FileIntegrityMonitor()

@app.route('/api/monitor-integrity', methods=['POST'])
def api_monitor_integrity():
    try:
        files = request.files.getlist('files')
        algorithm = request.form.get('algorithm', 'sha256')
        mode = request.form.get('mode', 'one-time')
        
        if not files:
            return jsonify({'error': 'No files provided'}), 400
        
        # Save files temporarily
        temp_files = []
        for file in files:
            temp_path = f"/tmp/{file.filename}"
            file.save(temp_path)
            temp_files.append(temp_path)
        
        # Monitor files
        results = monitor.monitor_files(temp_files, algorithm, mode)
        
        # Clean up
        for temp_path in temp_files:
            os.remove(temp_path)
        
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    with open('file-integrity-monitor.html', 'r') as f:
        return f.read()

if __name__ == '__main__':
    print("🔒 File Integrity Monitor Starting...")
    app.run(host='0.0.0.0', port=5004, debug=True)
