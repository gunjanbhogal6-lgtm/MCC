#!/bin/bash
echo "=== AutoSEO Dashboard Test Script ==="
echo ""

# Check if server is running
echo "1. Checking if server is running..."
if curl -s http://localhost:9100/health > /dev/null 2>&1; then
    echo "   ✓ Server is running on port 9100"
else
    echo "   ✗ Server not running. Starting..."
    uvicorn api:app --host 0.0.0.0 --port 9100 &
    sleep 3
fi

echo ""
echo "2. Testing API endpoints..."

# Test root endpoint
echo "   Testing / ..."
curl -s http://localhost:9100/ | python3 -m json.tool 2>/dev/null | head -5

# Test pipeline status
echo ""
echo "   Testing /pipeline/status ..."
curl -s http://localhost:9100/pipeline/status | python3 -m json.tool 2>/dev/null | head -10

# Test prompts endpoint
echo ""
echo "   Testing /dashboard/prompts ..."
curl -s http://localhost:9100/dashboard/prompts | python3 -m json.tool 2>/dev/null | head -10

# Test SEO comparison
echo ""
echo "   Testing /dashboard/seo-comparison ..."
curl -s http://localhost:9100/dashboard/seo-comparison | python3 -m json.tool 2>/dev/null | head -10

echo ""
echo "=== Dashboard URL ==="
echo "   http://localhost:9100/dashboard"
echo ""
echo "=== API Documentation ==="
echo "   http://localhost:9100/docs"
echo ""
