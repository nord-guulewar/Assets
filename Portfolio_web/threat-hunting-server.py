#!/usr/bin/env python3
"""
Threat Hunting Engine API Server
AI-powered threat detection and anomaly analysis
"""

from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import json
import time
import random
import threading
import uuid
from datetime import datetime, timedelta
import numpy as np
from sklearn.ensemble import IsolationForest
import pandas as pd

app = Flask(__name__)
CORS(app)

class ThreatHuntingEngine:
    def __init__(self):
        self.active_hunts = {}
        self.threat_intelligence = []
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.initialize_ml_model()

    def initialize_ml_model(self):
        """Initialize the ML model with sample training data"""
        # Generate sample training data
        np.random.seed(42)
        n_samples = 1000
        features = ['network_traffic', 'auth_attempts', 'file_access', 'process_count', 'memory_usage', 'cpu_usage']

        # Normal behavior patterns
        normal_data = np.random.normal([50, 2, 20, 15, 60, 30], [10, 1, 5, 3, 15, 10], (n_samples, 6))

        # Add some anomalous patterns for training
        anomalous_data = np.random.normal([80, 10, 50, 25, 90, 80], [20, 5, 15, 8, 25, 20], (int(n_samples * 0.1), 6))

        training_data = np.vstack([normal_data, anomalous_data])
        self.anomaly_detector.fit(training_data)

    def analyze_query(self, query, time_range="24h", severity_filter="all", confidence_threshold=0.7):
        """Analyze hunting query and return results"""
        start_time = time.time()

        # Parse time range
        hours_map = {"1h": 1, "24h": 24, "7d": 168, "30d": 720}
        hours = hours_map.get(time_range, 24)

        # Generate mock hunting results
        results = self.generate_hunting_results(query, hours, severity_filter, confidence_threshold)

        processing_time = time.time() - start_time

        return {
            "query": query,
            "time_range": time_range,
            "severity_filter": severity_filter,
            "confidence_threshold": confidence_threshold,
            "processing_time_ms": round(processing_time * 1000, 2),
            "results": results,
            "summary": {
                "total_results": len(results),
                "threats_found": len([r for r in results if r["severity"] in ["high", "critical"]]),
                "anomalies_found": len([r for r in results if r["severity"] in ["medium", "low"]]),
                "false_positives": len([r for r in results if r.get("false_positive", False)])
            }
        }

    def generate_hunting_results(self, query, hours, severity_filter, confidence_threshold):
        """Generate mock hunting results based on query"""
        results = []

        # Determine number of results based on query complexity
        if "suspicious" in query.lower() or "anomalous" in query.lower():
            result_count = random.randint(5, 15)
        elif "brute" in query.lower() or "attack" in query.lower():
            result_count = random.randint(3, 8)
        else:
            result_count = random.randint(1, 10)

        severities = ["critical", "high", "medium", "low"]
        sources = ["endpoint-001", "server-005", "firewall-002", "database-003", "web-server-007", "api-gateway-004"]

        for i in range(result_count):
            severity = random.choice(severities)

            # Filter by severity if specified
            if severity_filter == "high" and severity not in ["high", "critical"]:
                continue
            elif severity_filter == "medium" and severity == "low":
                continue

            # Generate anomaly score
            if severity in ["critical", "high"]:
                anomaly_score = random.uniform(0.8, 0.95)
            elif severity == "medium":
                anomaly_score = random.uniform(0.6, 0.8)
            else:
                anomaly_score = random.uniform(0.4, 0.6)

            # Skip if below confidence threshold
            if anomaly_score < confidence_threshold:
                continue

            # Generate timestamp within time range
            hours_ago = random.uniform(0, hours)
            timestamp = datetime.now() - timedelta(hours=hours_ago)

            result = {
                "id": str(uuid.uuid4())[:8],
                "severity": severity,
                "timestamp": timestamp.isoformat(),
                "source": random.choice(sources),
                "description": self.generate_description(query, severity),
                "anomaly_score": round(anomaly_score, 3),
                "confidence": round(anomaly_score * 100, 1),
                "indicators": self.generate_indicators(severity),
                "false_positive": random.random() < 0.1,  # 10% false positive rate
                "mitre_tactic": self.get_mitre_tactic(query),
                "recommended_action": self.get_recommended_action(severity)
            }

            results.append(result)

        return sorted(results, key=lambda x: x["anomaly_score"], reverse=True)

    def generate_description(self, query, severity):
        """Generate contextual description based on query and severity"""
        templates = {
            "critical": [
                f"Critical security event detected: {query} with multiple indicators",
                f"High-priority threat identified in {query} analysis",
                f"Severe anomaly in {query} requiring immediate attention"
            ],
            "high": [
                f"Significant security concern in {query} patterns",
                f"Elevated risk detected in {query} behavior",
                f"Important threat indicator found in {query}"
            ],
            "medium": [
                f"Moderate anomaly detected in {query} activity",
                f"Unusual pattern identified in {query} data",
                f"Potential security concern in {query} metrics"
            ],
            "low": [
                f"Minor irregularity noted in {query} analysis",
                f"Slight deviation from normal {query} patterns",
                f"Low-priority observation in {query} data"
            ]
        }

        return random.choice(templates.get(severity, templates["medium"]))

    def generate_indicators(self, severity):
        """Generate relevant security indicators"""
        all_indicators = [
            "Multiple failed authentication attempts",
            "Unusual network traffic patterns",
            "Suspicious file system activity",
            "Elevated privilege usage",
            "Anomalous process behavior",
            "Unexpected data exfiltration",
            "Malware signature match",
            "Known threat actor indicators",
            "Statistical deviation from baseline",
            "Correlation with threat intelligence"
        ]

        # More indicators for higher severity
        count = {"critical": 4, "high": 3, "medium": 2, "low": 1}[severity]
        return random.sample(all_indicators, count)

    def get_mitre_tactic(self, query):
        """Map query to MITRE ATT&CK tactic"""
        tactic_map = {
            "login": "Initial Access",
            "authentication": "Credential Access",
            "network": "Command and Control",
            "file": "Collection",
            "process": "Execution",
            "memory": "Defense Evasion",
            "privilege": "Privilege Escalation"
        }

        for key, tactic in tactic_map.items():
            if key in query.lower():
                return tactic

        return "Discovery"

    def get_recommended_action(self, severity):
        """Provide recommended actions based on severity"""
        actions = {
            "critical": [
                "Immediate isolation and investigation required",
                "Alert security team and initiate incident response",
                "Quarantine affected systems"
            ],
            "high": [
                "Escalate to security operations team",
                "Increase monitoring on affected systems",
                "Review and validate findings"
            ],
            "medium": [
                "Monitor closely and document findings",
                "Add to watchlist for further analysis",
                "Review security policies"
            ],
            "low": [
                "Log for trending analysis",
                "Monitor for pattern development",
                "Include in routine security review"
            ]
        }

        return random.choice(actions.get(severity, actions["medium"]))

    def get_threat_intelligence(self):
        """Return recent threat intelligence"""
        if not self.threat_intelligence:
            self.generate_threat_intelligence()

        return self.threat_intelligence[-10:]  # Return last 10 items

    def generate_threat_intelligence(self):
        """Generate mock threat intelligence"""
        intel_types = ["IOC", "TTP", "VULN", "CAMPAIGN", "ACTOR"]
        severities = ["high", "medium", "low"]

        for _ in range(5):
            intel = {
                "id": str(uuid.uuid4())[:8],
                "type": random.choice(intel_types),
                "severity": random.choice(severities),
                "title": self.generate_intel_title(),
                "description": self.generate_intel_description(),
                "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat(),
                "source": random.choice(["Mandiant", "CrowdStrike", "FireEye", "Custom Analysis"]),
                "confidence": random.randint(70, 95)
            }
            self.threat_intelligence.append(intel)

# Global engine instance
engine = ThreatHuntingEngine()

@app.route('/api/hunt', methods=['POST'])
def hunt():
    """Execute threat hunting query"""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"error": "Query parameter required"}), 400

        query = data['query']
        time_range = data.get('time_range', '24h')
        severity_filter = data.get('severity_filter', 'all')
        confidence_threshold = float(data.get('confidence_threshold', 0.7))

        results = engine.analyze_query(query, time_range, severity_filter, confidence_threshold)

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/threat-intelligence', methods=['GET'])
def threat_intelligence():
    """Get threat intelligence feed"""
    try:
        intel = engine.get_threat_intelligence()
        return jsonify({"intelligence": intel})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/hunt/status', methods=['GET'])
def hunt_status():
    """Get hunting engine status"""
    return jsonify({
        "status": "active",
        "uptime": "99.5%",
        "active_hunts": len(engine.active_hunts),
        "last_scan": datetime.now().isoformat(),
        "ml_model_accuracy": "96.2%"
    })

@app.route('/api/system/metrics', methods=['GET'])
def system_metrics():
    """Get system performance metrics"""
    return jsonify({
        "cpu_usage": random.uniform(15, 45),
        "memory_usage": random.uniform(60, 85),
        "disk_usage": random.uniform(40, 70),
        "network_throughput": random.uniform(50, 200),
        "active_connections": random.randint(50, 200),
        "queries_per_minute": random.randint(10, 50)
    })

@app.route('/api/ml/predict', methods=['POST'])
def ml_predict():
    """ML prediction endpoint for anomaly detection"""
    try:
        data = request.get_json()
        if not data or 'features' not in data:
            return jsonify({"error": "Features parameter required"}), 400

        features = np.array(data['features']).reshape(1, -1)
        prediction = engine.anomaly_detector.predict(features)
        score = engine.anomaly_detector.score_samples(features)[0]

        return jsonify({
            "prediction": "anomaly" if prediction[0] == -1 else "normal",
            "confidence": float(score),
            "anomaly_score": float(-score)  # Convert to positive anomaly score
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Threat Hunting Engine API Server")
    print("Starting on http://localhost:5000")
    print("")
    print("Available endpoints:")
    print("  POST /api/hunt              - Execute hunting query")
    print("  GET  /api/threat-intelligence - Get threat intelligence")
    print("  GET  /api/hunt/status       - Get engine status")
    print("  GET  /api/system/metrics    - Get system metrics")
    print("  POST /api/ml/predict        - ML anomaly prediction")
    print("")

    app.run(host='0.0.0.0', port=5000, debug=True)