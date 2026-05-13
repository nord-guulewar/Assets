#!/usr/bin/env python3
"""
Real Log Analysis Tool with File Processing and Regex Parsing
A production-ready security tool that actually processes log files and detects security events.
"""

import re
import json
import hashlib
import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from collections import defaultdict, Counter
import ipaddress
import urllib.parse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class LogAnalyzer:
    """Real log analyzer with file processing and regex pattern matching"""
    
    def __init__(self):
        self.patterns = self._load_patterns()
        self.security_patterns = self._load_security_patterns()
    
    def _load_patterns(self):
        """Load regex patterns for different log types"""
        return {
            'apache': [
                {
                    'name': 'HTTP Status Codes',
                    'regex': r'\s(4[0-9]{2}|5[0-9]{2})\s',
                    'description': 'HTTP error status codes (4xx, 5xx)'
                },
                {
                    'name': 'IP Addresses',
                    'regex': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
                    'description': 'IPv4 addresses'
                },
                {
                    'name': 'HTTP Methods',
                    'regex': r'"(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)',
                    'description': 'HTTP request methods'
                },
                {
                    'name': 'Response Sizes',
                    'regex': r'\s([0-9]+|-)\s*$',
                    'description': 'Response size in bytes'
                },
                {
                    'name': 'User Agents',
                    'regex': r'"([^"]*)"$',
                    'description': 'Browser/user agent strings'
                }
            ],
            'nginx': [
                {
                    'name': 'HTTP Status Codes',
                    'regex': r'\s(4[0-9]{2}|5[0-9]{2})\s',
                    'description': 'HTTP error status codes'
                },
                {
                    'name': 'Response Time',
                    'regex': r'\s([0-9]+\.[0-9]+)\s',
                    'description': 'Response time in seconds'
                },
                {
                    'name': 'Upstream Response Time',
                    'regex': r'upstream_response_time\s([0-9]+\.[0-9]+)',
                    'description': 'Upstream server response time'
                },
                {
                    'name': 'Request Length',
                    'regex': r'request_length\s([0-9]+)',
                    'description': 'HTTP request length'
                }
            ],
            'system': [
                {
                    'name': 'Process IDs',
                    'regex': r'\[(\d+)\]',
                    'description': 'System process IDs'
                },
                {
                    'name': 'Timestamps',
                    'regex': r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}',
                    'description': 'System timestamps'
                },
                {
                    'name': 'Error Levels',
                    'regex': r'(ERROR|WARN|INFO|DEBUG|CRITICAL)',
                    'description': 'Log severity levels'
                },
                {
                    'name': 'Memory Usage',
                    'regex': r'([0-9]+)KB|([0-9]+)MB|([0-9]+)GB',
                    'description': 'Memory usage patterns'
                }
            ],
            'auth': [
                {
                    'name': 'Failed Logins',
                    'regex': r'(failed|invalid|denied|authentication\sfailed)',
                    'description': 'Failed authentication attempts'
                },
                {
                    'name': 'User Names',
                    'regex': r'user\s+(\w+)',
                    'description': 'Username patterns'
                },
                {
                    'name': 'SSH Connections',
                    'regex': r'sshd.*from\s([0-9.]+)',
                    'description': 'SSH connection attempts'
                },
                {
                    'name': 'Session IDs',
                    'regex': r'session\s+([a-zA-Z0-9_-]+)',
                    'description': 'Session identifiers'
                }
            ],
            'firewall': [
                {
                    'name': 'Blocked Connections',
                    'regex': r'(blocked|denied|dropped|rejected)',
                    'description': 'Blocked network connections'
                },
                {
                    'name': 'Port Numbers',
                    'regex': r'port\s+(\d+)',
                    'description': 'Network port numbers'
                },
                {
                    'name': 'Protocol Types',
                    'regex': r'(TCP|UDP|ICMP|ESP|AH)',
                    'description': 'Network protocols'
                },
                {
                    'name': 'Interface Names',
                    'regex': r'interface\s+(\w+)',
                    'description': 'Network interface names'
                }
            ]
        }
    
    def _load_security_patterns(self):
        """Load security event detection patterns"""
        return [
            {
                'name': 'SQL Injection Attempts',
                'regex': r'(?i)(union\s+select|select\s+.*\s+from|insert\s+into|delete\s+from|drop\s+table|exec\s*\(|script\s*>|javascript:)',
                'severity': 'critical',
                'type': 'Injection Attack',
                'description': 'Potential SQL injection or script injection'
            },
            {
                'name': 'Cross-Site Scripting',
                'regex': r'(?i)(<script|<iframe|onload=|onerror=|javascript:|vbscript:)',
                'severity': 'high',
                'type': 'XSS Attack',
                'description': 'Cross-site scripting patterns'
            },
            {
                'name': 'Path Traversal',
                'regex': r'(\.\./|\.\.\\|%2e%2e%2f|%2e%2e%5c|%c0%af|%c1%9c)',
                'severity': 'high',
                'type': 'Path Traversal',
                'description': 'Directory traversal attempts'
            },
            {
                'name': 'Command Injection',
                'regex': r'(?i)(;|\||&|`|\$\(|\${|\$\[|\$\{|\$\()',
                'severity': 'critical',
                'type': 'Command Injection',
                'description': 'Command injection patterns'
            },
            {
                'name': 'Brute Force Attempts',
                'regex': r'(?i)(failed\s+login|authentication\s+failed|invalid\s+password|access\s+denied)',
                'severity': 'medium',
                'type': 'Brute Force',
                'description': 'Repeated authentication failures'
            },
            {
                'name': 'Suspicious User Agents',
                'regex': r'(?i)(sqlmap|nikto|nmap|curl|wget|python|perl|java|scanner|bot|crawler)',
                'severity': 'medium',
                'type': 'Suspicious Tool',
                'description': 'Automated scanning tools'
            },
            {
                'name': 'Large Payloads',
                'regex': r'(Content-Length:\s+[0-9]{4,}|request_body_size:\s+[0-9]{4,})',
                'severity': 'low',
                'type': 'Large Payload',
                'description': 'Unusually large request payloads'
            },
            {
                'name': 'Privilege Escalation',
                'regex': r'(?i)(sudo|su|root|admin|privilege|escalation|unauthorized\s+access)',
                'severity': 'high',
                'type': 'Privilege Escalation',
                'description': 'Privilege escalation attempts'
            }
        ]
    
    def analyze_log(self, content, filename, log_type, analysis_focus, custom_pattern=None):
        """Perform comprehensive log analysis"""
        
        try:
            lines = content.split('\n')
            
            # Basic statistics
            total_lines = len([line for line in lines if line.strip()])
            
            # Extract patterns
            pattern_matches = self._extract_patterns(lines, log_type, custom_pattern)
            
            # Detect security events
            security_events = self._detect_security_events(lines, analysis_focus)
            
            # Extract metrics
            summary = self._calculate_summary(lines, log_type)
            
            # Generate preview
            preview = '\n'.join(lines[:100])
            
            return {
                'summary': summary,
                'patternMatches': pattern_matches,
                'securityEvents': security_events,
                'preview': preview,
                'analysis': {
                    'fileHash': self._calculate_file_hash(content),
                    'analysisTime': datetime.now().isoformat(),
                    'logType': log_type,
                    'focus': analysis_focus
                }
            }
            
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            raise
    
    def _extract_patterns(self, lines, log_type, custom_pattern=None):
        """Extract patterns from log lines"""
        matches = []
        
        # Get patterns for the log type
        patterns = self.patterns.get(log_type, self.patterns['system'])
        
        # Add custom pattern if provided
        if custom_pattern:
            try:
                patterns.append({
                    'name': 'Custom Pattern',
                    'regex': custom_pattern,
                    'description': 'User-defined pattern'
                })
            except re.error:
                logger.warning("Invalid custom regex pattern")
        
        # Extract matches for each pattern
        for pattern in patterns:
            try:
                regex = re.compile(pattern['regex'], re.IGNORECASE)
                
                for line_num, line in enumerate(lines, 1):
                    if not line.strip():
                        continue
                    
                    line_matches = regex.finditer(line)
                    for match in line_matches:
                        matches.append({
                            'pattern': pattern['name'],
                            'description': pattern['description'],
                            'line': line_num,
                            'match': match.group(),
                            'context': line.strip()[:200] + ('...' if len(line.strip()) > 200 else ''),
                            'position': match.start()
                        })
                        
                        # Limit matches per pattern to avoid overwhelming results
                        if len(matches) > 1000:
                            break
                    
                    if len(matches) > 1000:
                        break
                        
            except re.error as e:
                logger.warning(f"Invalid regex in pattern {pattern['name']}: {e}")
                continue
            
            if len(matches) > 1000:
                break
        
        return matches[:500]  # Limit total matches
    
    def _detect_security_events(self, lines, analysis_focus):
        """Detect security events in log lines"""
        events = []
        
        for line_num, line in enumerate(lines, 1):
            if not line.strip():
                continue
            
            # Check against security patterns
            for pattern in self.security_patterns:
                try:
                    regex = re.compile(pattern['regex'], re.IGNORECASE)
                    if regex.search(line):
                        # Extract additional context
                        ip_addresses = self._extract_ip_addresses(line)
                        timestamps = self._extract_timestamps(line)
                        
                        events.append({
                            'line': line_num,
                            'severity': pattern['severity'],
                            'type': pattern['type'],
                            'pattern': pattern['name'],
                            'description': pattern['description'],
                            'context': line.strip()[:300] + ('...' if len(line.strip()) > 300 else ''),
                            'timestamp': timestamps[0] if timestamps else 'Unknown',
                            'ipAddresses': ip_addresses,
                            'riskScore': self._calculate_risk_score(pattern['severity'], len(ip_addresses))
                        })
                        
                except re.error:
                    continue
        
        # Sort by risk score (highest first)
        events.sort(key=lambda x: x['riskScore'], reverse=True)
        
        return events[:50]  # Limit to top 50 events
    
    def _extract_ip_addresses(self, line):
        """Extract IP addresses from a log line"""
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        return re.findall(ip_pattern, line)
    
    def _extract_timestamps(self, line):
        """Extract timestamps from a log line"""
        timestamp_patterns = [
            r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}',
            r'\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}',
            r'\w{3}\s\d{1,2}\s\d{2}:\d{2}:\d{2}',
            r'\d{4}/\d{2}/\d{2}\s\d{2}:\d{2}:\d{2}'
        ]
        
        for pattern in timestamp_patterns:
            match = re.search(pattern, line)
            if match:
                return [match.group()]
        
        return []
    
    def _calculate_risk_score(self, severity, ip_count):
        """Calculate risk score based on severity and context"""
        severity_scores = {'critical': 10, 'high': 7, 'medium': 4, 'low': 2}
        base_score = severity_scores.get(severity, 2)
        
        # Add points for multiple IP addresses (potential widespread attack)
        ip_bonus = min(ip_count * 0.5, 2)
        
        return base_score + ip_bonus
    
    def _calculate_summary(self, lines, log_type):
        """Calculate summary statistics"""
        non_empty_lines = [line for line in lines if line.strip()]
        
        # Count security events
        security_events = 0
        error_count = 0
        unique_ips = set()
        
        for line in non_empty_lines:
            # Count security events
            for pattern in self.security_patterns:
                try:
                    if re.search(pattern['regex'], line, re.IGNORECASE):
                        security_events += 1
                        break
                except re.error:
                    continue
            
            # Count errors
            if re.search(r'(error|failed|exception|critical|fatal)', line, re.IGNORECASE):
                error_count += 1
            
            # Extract unique IPs
            ips = self._extract_ip_addresses(line)
            unique_ips.update(ips)
        
        # Calculate additional metrics based on log type
        additional_metrics = self._calculate_type_specific_metrics(non_empty_lines, log_type)
        
        return {
            'totalLines': len(non_empty_lines),
            'securityEvents': security_events,
            'errors': error_count,
            'uniqueIPs': len(unique_ips),
            **additional_metrics
        }
    
    def _calculate_type_specific_metrics(self, lines, log_type):
        """Calculate metrics specific to log types"""
        metrics = {}
        
        if log_type in ['apache', 'nginx']:
            # HTTP status code distribution
            status_codes = Counter()
            response_times = []
            
            for line in lines:
                # Extract status codes
                status_match = re.search(r'\s([0-9]{3})\s', line)
                if status_match:
                    status_codes[status_match.group(1)] += 1
                
                # Extract response times (nginx)
                time_match = re.search(r'\s([0-9]+\.[0-9]+)\s', line)
                if time_match:
                    try:
                        response_times.append(float(time_match.group(1)))
                    except ValueError:
                        pass
            
            metrics['statusCodes'] = dict(status_codes.most_common(10))
            if response_times:
                metrics['avgResponseTime'] = sum(response_times) / len(response_times)
                metrics['maxResponseTime'] = max(response_times)
        
        elif log_type == 'auth':
            # Authentication metrics
            failed_logins = 0
            successful_logins = 0
            unique_users = set()
            
            for line in lines:
                if re.search(r'(failed|denied|invalid)', line, re.IGNORECASE):
                    failed_logins += 1
                elif re.search(r'(accepted|success|granted)', line, re.IGNORECASE):
                    successful_logins += 1
                
                # Extract usernames
                user_match = re.search(r'user\s+(\w+)', line, re.IGNORECASE)
                if user_match:
                    unique_users.add(user_match.group(1))
            
            metrics['failedLogins'] = failed_logins
            metrics['successfulLogins'] = successful_logins
            metrics['uniqueUsers'] = len(unique_users)
        
        return metrics
    
    def _calculate_file_hash(self, content):
        """Calculate SHA-256 hash of file content"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

# Initialize analyzer
analyzer = LogAnalyzer()

@app.route('/api/analyze-log', methods=['POST'])
def api_analyze_log():
    """API endpoint for log analysis"""
    try:
        data = request.get_json()
        
        content = data.get('content', '')
        filename = data.get('fileName', 'unknown')
        log_type = data.get('logType', 'system')
        analysis_focus = data.get('analysisFocus', 'comprehensive')
        custom_pattern = data.get('customPattern')
        
        if not content.strip():
            return jsonify({'error': 'Log content is required'}), 400
        
        # Validate content size (limit to 50MB)
        if len(content.encode('utf-8')) > 50 * 1024 * 1024:
            return jsonify({'error': 'File too large (max 50MB)'}), 400
        
        # Perform analysis
        results = analyzer.analyze_log(content, filename, log_type, analysis_focus, custom_pattern)
        
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def api_status():
    """Check analyzer status"""
    return jsonify({
        'analyzer': 'Log Analysis Tool',
        'version': '1.0.0',
        'patterns_loaded': len(analyzer.patterns),
        'security_patterns': len(analyzer.security_patterns),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/')
def index():
    """Serve the log analyzer interface"""
    with open('log-analyzer.html', 'r') as f:
        return f.read()

if __name__ == '__main__':
    print("📊 Log Analysis Tool Starting...")
    print(f"🔍 Patterns loaded: {len(analyzer.patterns)} log types")
    print(f"🛡️  Security patterns: {len(analyzer.security_patterns)}")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
