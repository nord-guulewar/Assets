#!/bin/bash

# Advanced SecOps Tools Deployment Script
# This script deploys all 5 security tools with their backends

set -e

echo "🚀 Starting Advanced SecOps Tools Deployment"
echo "=============================================="

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create necessary directories for volume mounts
echo "📁 Creating backend directories..."
mkdir -p soar-backend compliance-backend

# Create placeholder files for .NET services
echo "🔧 Setting up .NET backend placeholders..."
cat > soar-backend/Program.cs << 'EOF'
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Hosting;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/api/soar/status", () => new {
    status = "running",
    workflows = 12,
    integrations = 8,
    uptime = "99.5%"
});

app.MapGet("/api/soar/workflows", () => new[] {
    new { id = "wf-001", name = "Phishing Response", status = "active" },
    new { id = "wf-002", name = "Ransomware Response", status = "active" }
});

app.Run();
EOF

cat > soar-backend/soar-backend.csproj << 'EOF'
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net7.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
</Project>
EOF

cat > compliance-backend/Program.cs << 'EOF'
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Hosting;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/api/compliance/status", () => new {
    status = "running",
    frameworks = 8,
    assessments = 245,
    compliance_score = 87.3
});

app.MapGet("/api/compliance/frameworks", () => new[] {
    new { name = "SOC 2", score = 95, status = "compliant" },
    new { name = "ISO 27001", score = 92, status = "compliant" },
    new { name = "GDPR", score = 88, status = "compliant" }
});

app.Run();
EOF

cat > compliance-backend/compliance-backend.csproj << 'EOF'
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net7.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
</Project>
EOF

# Build and start all services
echo "🏗️  Building and starting services..."
docker-compose up --build -d

echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
echo "🔍 Checking service health..."

check_service() {
    local service=$1
    local url=$2
    local name=$3

    if curl -f -s "$url" > /dev/null 2>&1; then
        echo "✅ $name is running"
    else
        echo "❌ $name failed to start"
        return 1
    fi
}

# Check each service
check_service "siem" "http://localhost/api/siem/metrics" "SIEM Dashboard"
check_service "threat" "http://localhost/api/threat/hunt/status" "Threat Hunting Engine"
check_service "soar" "http://localhost/api/soar/status" "SOAR Platform"
check_service "compliance" "http://localhost/api/compliance/status" "Compliance Suite"
check_service "ztna" "http://localhost/api/ztna/status" "ZTNA Gateway"

echo ""
echo "🎉 Deployment Complete!"
echo "=========================="
echo ""
echo "Your Advanced SecOps Tools are now running:"
echo ""
echo "🌐 Frontend:      http://localhost"
echo "📊 SIEM:          http://localhost/siem-dashboard.html"
echo "🔍 Threat Hunt:   http://localhost/threat-hunting.html"
echo "⚡ SOAR:           http://localhost/soar-platform.html"
echo "📋 Compliance:    http://localhost/compliance-suite.html"
echo "🔐 ZTNA:          http://localhost/ztna-gateway.html"
echo ""
echo "API Endpoints:"
echo "🔗 SIEM API:      http://localhost/api/siem/"
echo "🔗 Threat API:    http://localhost/api/threat/"
echo "🔗 SOAR API:      http://localhost/api/soar/"
echo "🔗 Compliance API: http://localhost/api/compliance/"
echo "🔗 ZTNA API:      http://localhost/api/ztna/"
echo ""
echo "To stop all services: docker-compose down"
echo "To view logs: docker-compose logs -f [service-name]"
echo ""
echo "Happy securing! 🛡️"