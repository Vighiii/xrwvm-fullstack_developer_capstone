#!/bin/bash

echo "🌐 Cloud Environment Setup Guide"
echo "================================"

echo ""
echo "📋 Step-by-Step Cloud Access Setup:"
echo ""

echo "1️⃣  EXPOSE PORTS IN YOUR CLOUD IDE:"
echo "   In your IDE interface, look for one of these:"
echo "   • 'Ports' tab/panel (usually at bottom)"
echo "   • 'Remote Explorer' → 'Ports'"
echo "   • 'Terminal' → 'Ports'"
echo "   • Menu → 'Terminal' → 'New Port'"
echo ""

echo "2️⃣  ADD THESE PORTS:"
echo "   Port 8000 - Django Application"
echo "   Port 3030 - API Service"
echo "   Port 27017 - MongoDB (optional)"
echo ""

echo "3️⃣  SET PORT VISIBILITY:"
echo "   Make sure ports are set to 'Public' or 'Open to Internet'"
echo ""

echo "4️⃣  ACCESS YOUR APPLICATION:"
echo "   Your IDE should provide URLs like:"
echo "   • https://your-workspace-8000.your-cloud-domain.com"
echo "   • https://your-workspace-3030.your-cloud-domain.com"
echo ""

echo "5️⃣  IF YOU SEE PROXY ERRORS:"
echo "   • Wait 30-60 seconds after opening ports"
echo "   • Refresh your browser"
echo "   • Try the 'Open in Browser' button in your IDE"
echo ""

echo "📊 Current Container Status:"
docker-compose ps

echo ""
echo "🔧 Alternative Methods:"
echo ""
echo "METHOD 1 - IDE Preview:"
echo "• Look for 'Preview' or 'Simple Browser' in your IDE"
echo "• Open: http://localhost:8000"
echo ""

echo "METHOD 2 - Port Forwarding Commands:"
echo "• Some IDEs use commands like:"
echo "  gp preview \$(gp url 8000)  # For Gitpod"
echo "  code --open-url http://localhost:8000  # For some VS Code environments"
echo ""

echo "METHOD 3 - Manual URL Construction:"
echo "• If your workspace URL is: https://workspace.domain.com"
echo "• Try: https://workspace-8000.domain.com"
echo "• Or: https://8000-workspace.domain.com"
echo ""

echo "🆘 If Still Having Issues:"
echo "1. Check IDE documentation for port forwarding"
echo "2. Look for 'Application' or 'Web Preview' features"
echo "3. Try restarting containers: docker-compose restart"
echo "4. Check firewall/network settings in your cloud provider"
echo ""

echo "✅ Your application IS working - it just needs proper port exposure!"
echo ""
