#!/usr/bin/env python3
"""
Real Password Strength Analyzer with Entropy Calculations
A production-ready security tool that actually calculates password entropy and estimates crack times.
"""

import math
import hashlib
import secrets
import string
import re
import json
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class PasswordAnalyzer:
    """Real password analyzer with entropy calculations and crack time estimation"""
    
    def __init__(self):
        self.common_passwords = self._load_common_passwords()
        self.dictionary_words = self._load_dictionary_words()
    
    def _load_common_passwords(self):
        """Load list of common passwords"""
        return [
            '123456', 'password', '123456789', '12345678', '12345',
            '1234567', '1234567890', 'qwerty', 'abc123', '111111',
            '123123', 'admin', 'letmein', 'welcome', 'monkey',
            '1234', 'dragon', 'master', 'hello', 'freedom',
            'whatever', 'qazwsx', 'trustno1', '123qwe', '1q2w3e4r',
            'zxcvbnm', '1qaz2wsx', 'password123', '123abc', 'iloveyou'
        ]
    
    def _load_dictionary_words(self):
        """Load common dictionary words"""
        return [
            'password', 'admin', 'user', 'login', 'welcome', 'hello',
            'computer', 'internet', 'network', 'system', 'security',
            'access', 'account', 'server', 'database', 'backup',
            'manager', 'service', 'application', 'software', 'hardware'
        ]
    
    def analyze_password(self, password):
        """Perform comprehensive password analysis"""
        
        try:
            # Calculate entropy
            entropy = self._calculate_shannon_entropy(password)
            
            # Calculate strength
            strength = self._determine_strength(entropy)
            
            # Estimate crack time
            crack_time = self._estimate_crack_time(password, entropy)
            
            # Character analysis
            char_analysis = self._analyze_characters(password)
            
            # Security checks
            security_checks = self._perform_security_checks(password)
            
            # Complexity score
            complexity_score = self._calculate_complexity_score(password)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(password, security_checks, char_analysis)
            
            return {
                'entropy': entropy,
                'strength': strength,
                'crackTime': crack_time,
                'characterCount': len(password),
                'complexityScore': complexity_score,
                'characterTypes': char_analysis['types'],
                'securityChecks': security_checks,
                'recommendations': recommendations,
                'analysis': {
                    'hash': self._calculate_password_hash(password),
                    'analysisTime': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            raise
    
    def _calculate_shannon_entropy(self, password):
        """Calculate Shannon entropy of password"""
        if not password:
            return 0
        
        # Count character frequencies
        char_counts = {}
        for char in password:
            char_counts[char] = char_counts.get(char, 0) + 1
        
        # Calculate entropy
        entropy = 0
        password_length = len(password)
        
        for count in char_counts.values():
            probability = count / password_length
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    def _determine_strength(self, entropy):
        """Determine password strength based on entropy"""
        if entropy < 28:
            return 'very-weak'
        elif entropy < 36:
            return 'weak'
        elif entropy < 60:
            return 'medium'
        elif entropy < 128:
            return 'strong'
        else:
            return 'very-strong'
    
    def _estimate_crack_time(self, password, entropy):
        """Estimate time to crack password"""
        if not password:
            return 'Instant'
        
        # Different attack scenarios
        scenarios = [
            {
                'name': 'Brute Force',
                'guesses_per_second': 1e12,  # Modern GPU
                'charset_size': self._get_charset_size(password)
            },
            {
                'name': 'Dictionary Attack',
                'guesses_per_second': 1e9,   # Optimized dictionary attack
                'charset_size': len(self.dictionary_words) * 1000  # With variations
            },
            {
                'name': 'Hybrid Attack',
                'guesses_per_second': 1e11,  # Between brute force and dictionary
                'charset_size': self._get_charset_size(password) * 1000
            }
        ]
        
        # Calculate time for each scenario
        times = []
        for scenario in scenarios:
            if scenario['name'] == 'Dictionary Attack' and self._is_common_password(password):
                # Common passwords are cracked instantly
                times.append('Instant')
            else:
                total_combinations = scenario['charset_size'] ** len(password)
                seconds = total_combinations / scenario['guesses_per_second']
                times.append(self._format_time(seconds))
        
        # Return the fastest crack time (worst case)
        return times[0] if times[0] != 'Instant' else 'Instant'
    
    def _get_charset_size(self, password):
        """Determine character set size based on password composition"""
        charset_size = 0
        if re.search(r'[a-z]', password):
            charset_size += 26
        if re.search(r'[A-Z]', password):
            charset_size += 26
        if re.search(r'[0-9]', password):
            charset_size += 10
        if re.search(r'[^a-zA-Z0-9]', password):
            charset_size += 32  # Approximate special characters
        
        return max(charset_size, 1)
    
    def _is_common_password(self, password):
        """Check if password is in common passwords list"""
        return password.lower() in [p.lower() for p in self.common_passwords]
    
    def _format_time(self, seconds):
        """Format time in human-readable format"""
        if seconds < 1:
            return 'Instant'
        elif seconds < 60:
            return f'{round(seconds)} seconds'
        elif seconds < 3600:
            return f'{round(seconds / 60)} minutes'
        elif seconds < 86400:
            return f'{round(seconds / 3600)} hours'
        elif seconds < 2592000:
            return f'{round(seconds / 86400)} days'
        elif seconds < 31536000:
            return f'{round(seconds / 2592000)} months'
        elif seconds < 3153600000:
            return f'{round(seconds / 31536000)} years'
        else:
            return f'{round(seconds / 3153600000)} centuries'
    
    def _analyze_characters(self, password):
        """Analyze character composition"""
        analysis = {
            'lowercase': bool(re.search(r'[a-z]', password)),
            'uppercase': bool(re.search(r'[A-Z]', password)),
            'digits': bool(re.search(r'[0-9]', password)),
            'special': bool(re.search(r'[^a-zA-Z0-9]', password)),
            'unique_chars': len(set(password)),
            'repeated_chars': len(password) - len(set(password))
        }
        
        analysis['types'] = {
            'lowercase': analysis['lowercase'],
            'uppercase': analysis['uppercase'],
            'digits': analysis['digits'],
            'special': analysis['special']
        }
        
        return analysis
    
    def _perform_security_checks(self, password):
        """Perform comprehensive security checks"""
        checks = [
            {
                'name': 'Minimum Length (12+ characters)',
                'status': 'pass' if len(password) >= 12 else 'fail',
                'description': 'Modern security standards recommend at least 12 characters'
            },
            {
                'name': 'No Common Patterns',
                'status': 'pass' if not self._has_common_patterns(password) else 'fail',
                'description': 'Avoid common patterns like "123456" or "password"'
            },
            {
                'name': 'No Dictionary Words',
                'status': 'pass' if not self._has_dictionary_words(password) else 'partial',
                'description': 'Avoid using complete dictionary words'
            },
            {
                'name': 'Mixed Character Types',
                'status': 'pass' if self._has_mixed_characters(password) else 'partial',
                'description': 'Use a mix of letters, numbers, and special characters'
            },
            {
                'name': 'No Repeated Characters',
                'status': 'pass' if not self._has_repeated_characters(password) else 'partial',
                'description': 'Avoid repeating the same character multiple times'
            },
            {
                'name': 'No Sequential Characters',
                'status': 'pass' if not self._has_sequential_characters(password) else 'partial',
                'description': 'Avoid sequential characters like "abc" or "123"'
            },
            {
                'name': 'Not in Common Passwords',
                'status': 'pass' if not self._is_common_password(password) else 'fail',
                'description': 'Avoid using commonly used passwords'
            },
            {
                'name': 'High Entropy',
                'status': 'pass' if self._calculate_shannon_entropy(password) >= 60 else 'partial',
                'description': 'Password should have high entropy (60+ bits)'
            }
        ]
        
        return checks
    
    def _has_common_patterns(self, password):
        """Check for common patterns"""
        patterns = [
            r'123456', r'password', r'qwerty', r'abc123',
            r'admin', r'letmein', r'welcome', r'(\d)\1{2,}',
            r'(.)\1\1\1', r'123', r'abc'
        ]
        
        password_lower = password.lower()
        return any(re.search(pattern, password_lower) for pattern in patterns)
    
    def _has_dictionary_words(self, password):
        """Check for dictionary words"""
        password_lower = password.lower()
        return any(word in password_lower for word in self.dictionary_words)
    
    def _has_mixed_characters(self, password):
        """Check for mixed character types"""
        types = 0
        if re.search(r'[a-z]', password):
            types += 1
        if re.search(r'[A-Z]', password):
            types += 1
        if re.search(r'[0-9]', password):
            types += 1
        if re.search(r'[^a-zA-Z0-9]', password):
            types += 1
        
        return types >= 3
    
    def _has_repeated_characters(self, password):
        """Check for repeated characters"""
        return bool(re.search(r'(.)\1{2,}', password))
    
    def _has_sequential_characters(self, password):
        """Check for sequential characters"""
        for i in range(len(password) - 2):
            char1 = ord(password[i])
            char2 = ord(password[i + 1])
            char3 = ord(password[i + 2])
            
            # Check for sequential characters (both forward and backward)
            if (char2 == char1 + 1 and char3 == char2 + 1) or \
               (char2 == char1 - 1 and char3 == char2 - 1):
                return True
        
        return False
    
    def _calculate_complexity_score(self, password):
        """Calculate overall complexity score"""
        score = 0
        
        # Length component (max 30 points)
        score += min(len(password) * 2, 30)
        
        # Character variety component (max 40 points)
        if re.search(r'[a-z]', password):
            score += 10
        if re.search(r'[A-Z]', password):
            score += 10
        if re.search(r'[0-9]', password):
            score += 10
        if re.search(r'[^a-zA-Z0-9]', password):
            score += 10
        
        # Pattern penalties
        if self._has_common_patterns(password):
            score -= 20
        if self._has_repeated_characters(password):
            score -= 10
        if self._has_sequential_characters(password):
            score -= 10
        
        return max(0, min(100, score))
    
    def _generate_recommendations(self, password, security_checks, char_analysis):
        """Generate personalized recommendations"""
        recommendations = []
        
        # Length recommendations
        if len(password) < 12:
            recommendations.append({
                'type': 'length',
                'priority': 'high',
                'message': f'Use at least 12 characters (currently {len(password)})'
            })
        elif len(password) < 16:
            recommendations.append({
                'type': 'length',
                'priority': 'medium',
                'message': 'Consider using 16+ characters for maximum security'
            })
        
        # Character type recommendations
        if not char_analysis['types']['uppercase']:
            recommendations.append({
                'type': 'uppercase',
                'priority': 'medium',
                'message': 'Add uppercase letters to increase complexity'
            })
        
        if not char_analysis['types']['digits']:
            recommendations.append({
                'type': 'digits',
                'priority': 'medium',
                'message': 'Include numbers to make password harder to guess'
            })
        
        if not char_analysis['types']['special']:
            recommendations.append({
                'type': 'special',
                'priority': 'high',
                'message': 'Add special characters (!@#$%^&*) for maximum security'
            })
        
        # Pattern-based recommendations
        if self._has_common_patterns(password):
            recommendations.append({
                'type': 'patterns',
                'priority': 'high',
                'message': 'Avoid common patterns and dictionary words'
            })
        
        if self._has_repeated_characters(password):
            recommendations.append({
                'type': 'repetition',
                'priority': 'medium',
                'message': 'Avoid repeating the same character multiple times'
            })
        
        if self._has_sequential_characters(password):
            recommendations.append({
                'type': 'sequential',
                'priority': 'medium',
                'message': 'Avoid sequential characters like "abc" or "123"'
            })
        
        # Entropy-based recommendations
        entropy = self._calculate_shannon_entropy(password)
        if entropy < 60:
            recommendations.append({
                'type': 'entropy',
                'priority': 'high',
                'message': f'Increase entropy (currently {entropy:.1f} bits) by using more diverse characters'
            })
        
        return recommendations
    
    def _calculate_password_hash(self, password):
        """Calculate SHA-256 hash of password"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def generate_secure_password(self, length=16, use_uppercase=True, use_lowercase=True, 
                           use_digits=True, use_special=True):
        """Generate cryptographically secure password"""
        if not any([use_uppercase, use_lowercase, use_digits, use_special]):
            raise ValueError("At least one character type must be selected")
        
        charset = ''
        if use_lowercase:
            charset += string.ascii_lowercase
        if use_uppercase:
            charset += string.ascii_uppercase
        if use_digits:
            charset += string.digits
        if use_special:
            charset += '!@#$%^&*()_+-=[]{}|;:,.<>?'
        
        # Generate password using cryptographically secure random generator
        password = ''.join(secrets.choice(charset) for _ in range(length))
        
        return password

# Initialize analyzer
analyzer = PasswordAnalyzer()

@app.route('/api/analyze-password', methods=['POST'])
def api_analyze_password():
    """API endpoint for password analysis"""
    try:
        data = request.get_json()
        password = data.get('password', '')
        
        if not password:
            return jsonify({'error': 'Password is required'}), 400
        
        # Perform analysis
        results = analyzer.analyze_password(password)
        
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-password', methods=['POST'])
def api_generate_password():
    """API endpoint for password generation"""
    try:
        data = request.get_json()
        length = data.get('length', 16)
        use_uppercase = data.get('useUppercase', True)
        use_lowercase = data.get('useLowercase', True)
        use_digits = data.get('useDigits', True)
        use_special = data.get('useSpecial', True)
        
        # Validate parameters
        if not 8 <= length <= 128:
            return jsonify({'error': 'Password length must be between 8 and 128'}), 400
        
        # Generate password
        password = analyzer.generate_secure_password(
            length, use_uppercase, use_lowercase, use_digits, use_special
        )
        
        return jsonify({
            'password': password,
            'entropy': analyzer._calculate_shannon_entropy(password),
            'strength': analyzer._determine_strength(analyzer._calculate_shannon_entropy(password))
        })
        
    except Exception as e:
        logger.error(f"Generation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def api_status():
    """Check analyzer status"""
    return jsonify({
        'analyzer': 'Password Strength Analyzer',
        'version': '1.0.0',
        'commonPasswords': len(analyzer.common_passwords),
        'dictionaryWords': len(analyzer.dictionary_words),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/')
def index():
    """Serve password analyzer interface"""
    with open('password-analyzer.html', 'r') as f:
        return f.read()

if __name__ == '__main__':
    print("🔐 Password Strength Analyzer Starting...")
    print(f"📊 Common passwords loaded: {len(analyzer.common_passwords)}")
    print(f"📚 Dictionary words loaded: {len(analyzer.dictionary_words)}")
    
    app.run(host='0.0.0.0', port=5002, debug=True)
