# Open-SEO Setup for QLUU

## Quick Start

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- [DataForSEO](https://app.dataforseo.com) account (free signup, pay-as-you-go API)

### Step 1: Get Your DataForSEO API Key
1. Go to https://app.dataforseo.com/api-access
2. Request credentials via email
3. You'll get a `login` and `password`
4. Encode them:
   ```bash
   printf '%s' 'YOUR_LOGIN:YOUR_PASSWORD' | base64
   ```
5. Copy the base64 output — this is your `DATAFORSEO_API_KEY`

### Step 2: Configure
Edit the `.env` file in this directory:
```
DATAFORSEO_API_KEY=YOUR_BASE64_ENCODED_KEY_HERE
```

### Step 3: Launch
```bash
cd open-seo
docker compose up -d
```

### Step 4: Access
Open http://localhost:3001

### First-Time Setup
1. **Add domain**: `qluulab.com`
2. **Run site audit**
3. **Add seed keywords**:
   - counter-UAS
   - C-UAS solutions
   - anti-drone defense
   - autonomous drone defense
   - AI airspace security
   - drone threat detection
   - sovereign AI defense
   - counter-UAS software
4. **Add competitors**:
   - dedrone.com
   - droneshield.com
   - anduril.com
   - shield.ai
   - fortemtech.com
   - citadeldefense.com
5. **Run backlink report** for qluulab.com

### Weekly Use (5 minutes)
Every Friday:
1. Check keyword ranking changes
2. Note any new backlinks won/lost
3. Review any site audit warnings

### Costs
- Docker hosting: **$0** (runs on your machine)
- DataForSEO API: ~**$5-15/month** with moderate use
- No subscription fees
