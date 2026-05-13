# Real Security Tools - Deployment Ready

A collection of production-ready security tools with actual functionality, not demos. These tools perform real security operations including network scanning, log analysis, password strength assessment, SSL/TLS validation, and file integrity monitoring.

## 🛡️ Security Tools Overview

### 1. Network Vulnerability Scanner (Port 5000)
**Real Nmap Integration**
- Performs actual network vulnerability scans using Nmap
- Detects open ports, services, and security vulnerabilities
- Supports multiple scan types: basic, comprehensive, vulnerability detection, stealth
- MITRE ATT&CK mapping for detected threats
- Export functionality for scan results

**Backend:** `scanner_backend.py`  
**Frontend:** `network-scanner.html`

**API Endpoints:**
- `POST /api/scan` - Perform network scan
  ```json
  {
    "target": "192.168.1.1",
    "scanType": "comprehensive",
    "portRange": "common",
    "customPorts": "80,443,22"
  }
  ```
- `GET /api/status` - Check scanner status

### 2. Log Analysis Tool (Port 5001)
**Real File Processing & Regex Parsing**
- Processes actual log files with regex pattern matching
- Detects security events, errors, and anomalies
- Supports multiple log formats: Apache, Nginx, System, Auth, Firewall
- Custom pattern matching capabilities
- Real-time security event detection

**Backend:** `log-analyzer-backend.py`  
**Frontend:** `log-analyzer.html`

**API Endpoints:**
- `POST /api/analyze-log` - Analyze log file
  ```json
  {
    "content": "log file content...",
    "fileName": "access.log",
    "logType": "apache",
    "analysisFocus": "security",
    "customPattern": "regex pattern"
  }
  ```
- `GET /api/status` - Check analyzer status

### 3. Password Strength Analyzer (Port 5002)
**Real Entropy Calculations**
- Calculates actual Shannon entropy for passwords
- Estimates real crack time based on GPU capabilities
- Performs comprehensive security checks
- Generates cryptographically secure passwords
- Real complexity scoring algorithms

**Backend:** `password-analyzer-backend.py`  
**Frontend:** `password-analyzer.html`

**API Endpoints:**
- `POST /api/analyze-password` - Analyze password strength
  ```json
  {
    "password": "MySecureP@ssw0rd123!"
  }
  ```
- `POST /api/generate-password` - Generate secure password
  ```json
  {
    "length": 16,
    "useUppercase": true,
    "useLowercase": true,
    "useDigits": true,
    "useSpecial": true
  }
  ```
- `GET /api/status` - Check analyzer status

### 4. SSL/TLS Certificate Checker (Port 5003)
**Real OpenSSL Validation**
- Validates SSL/TLS certificates using OpenSSL
- Checks certificate chain and trust
- Detects expired or expiring certificates
- Analyzes TLS protocol versions and cipher suites
- Real certificate fingerprint calculation

**Backend:** `ssl-checker-backend.py`  
**Frontend:** `ssl-checker.html`

**API Endpoints:**
- `POST /api/check-ssl` - Check SSL certificate
  ```json
  {
    "domain": "example.com",
    "port": 443
  }
  ```
- `GET /api/status` - Check checker status

### 5. File Integrity Monitor (Port 5004)
**Real Hash Verification**
- Calculates actual file hashes (SHA-256, SHA-512, MD5)
- Detects file modifications and integrity violations
- Supports continuous monitoring mode
- Baseline comparison for change detection
- Real-time integrity alerts

**Backend:** `file-integrity-backend.py`  
**Frontend:** `file-integrity-monitor.html`

**API Endpoints:**
- `POST /api/monitor-integrity` - Monitor file integrity
  ```json
  Form data with files, algorithm, and mode
  ```
- `GET /api/status` - Check monitor status

## 🚀 Deployment

### Prerequisites
- Docker and Docker Compose
- Python 3.9+
- Nmap (for network scanner)
- OpenSSL (for SSL checker)

### Quick Start with Docker

1. **Clone the repository**
```bash
git clone <repository-url>
cd Assets
```

2. **Build and start all services**
```bash
docker-compose up -d
```

3. **Access the tools**
- Network Scanner: http://localhost:5000
- Log Analyzer: http://localhost:5001
- Password Analyzer: http://localhost:5002
- SSL Checker: http://localhost:5003
- File Integrity Monitor: http://localhost:5004

### Manual Deployment

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Install system tools**
```bash
# Ubuntu/Debian
sudo apt-get install nmap openssl

# macOS
brew install nmap openssl

# Windows
# Download and install from official websites
```

3. **Run individual tools**
```bash
# Network Scanner
python scanner_backend.py

# Log Analyzer
python log-analyzer-backend.py

# Password Analyzer
python password-analyzer-backend.py

# SSL Checker
python ssl-checker-backend.py

# File Integrity Monitor
python file-integrity-backend.py
```

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Nginx Frontend (Port 80)              │
│              Serves static HTML/CSS/JS files            │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐  ┌──────▼────────┐  ┌──────▼────────┐
│ Network Scanner │  │ Log Analyzer  │  │ Password      │
│   Port 5000     │  │   Port 5001   │  │ Analyzer 5002 │
│   + Nmap        │  │   + Regex     │  │   + Entropy   │
└─────────────────┘  └───────────────┘  └───────────────┘
        │                   │                   │
┌───────▼────────┐  ┌──────▼────────┐  ┌──────▼────────┐
│ SSL Checker    │  │ File Integrity │  │               │
│   Port 5003    │  │   Monitor 5004 │  │               │
│   + OpenSSL    │  │   + Hash Calc  │  │               │
└─────────────────┘  └───────────────┘  └───────────────┘
```

## 🔒 Security Features

- **Real Nmap Integration**: Actual network vulnerability scanning
- **Regex Pattern Matching**: Real log analysis with custom patterns
- **Shannon Entropy**: Mathematical password strength calculation
- **OpenSSL Validation**: Certificate chain verification
- **Hash Verification**: SHA-256/SHA-512 file integrity checking
- **No Mock Data**: All tools perform actual security operations

## 📝 API Documentation

### Response Format

All APIs return JSON responses with the following structure:

**Success Response:**
```json
{
  "data": { ... },
  "status": "success"
}
```

**Error Response:**
```json
{
  "error": "Error message",
  "status": "error"
}
```

### Authentication

Currently, all tools run without authentication for demonstration purposes. For production deployment, implement:
- API key authentication
- Rate limiting
- Input validation
- CORS configuration

## 🛠️ Configuration

### Environment Variables

- `FLASK_ENV`: Set to `production` for production deployment
- `FLASK_DEBUG`: Set to `0` for production
- Custom ports can be configured in `docker-compose.yml`

### Tool-Specific Configuration

Each tool has its own configuration options accessible through the web interface or API parameters.

## 📈 Monitoring

### Health Checks

Each service includes a health check endpoint:
- `GET /api/status` - Returns service status and capabilities

### Docker Health Checks

All services include Docker health checks that monitor service availability.

## 🔧 Troubleshooting

### Common Issues

1. **Nmap not found**
   - Install Nmap: `sudo apt-get install nmap`
   - Tools will fall back to demo mode if Nmap is unavailable

2. **OpenSSL not found**
   - Install OpenSSL: `sudo apt-get install openssl`
   - Tools will use Python SSL module as fallback

3. **Port conflicts**
   - Change ports in `docker-compose.yml`
   - Ensure no other services are using the same ports

4. **Permission errors**
   - Ensure proper file permissions for log files and directories
   - Run with appropriate user permissions

## 📄 License

This project is for educational and demonstration purposes. Use responsibly and only on systems you have authorization to scan or monitor.

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:
- Test all changes thoroughly
- Update documentation
- Follow security best practices
- Ensure no sensitive data is included

## 📞 Support

For issues or questions:
- Check the troubleshooting section
- Review API documentation
- Examine logs for error messages

## 🎯 Use Cases

- **Security Auditing**: Perform real vulnerability assessments
- **Log Analysis**: Analyze actual log files for security events
- **Password Policy**: Enforce strong password requirements
- **Certificate Management**: Monitor SSL/TLS certificate expiry
- **File Integrity**: Detect unauthorized file modifications

## ⚠️ Disclaimer

These tools are provided for legitimate security testing and monitoring purposes only. Users are responsible for ensuring they have proper authorization before scanning or monitoring any systems. Unauthorized use of these tools may be illegal.
