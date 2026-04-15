# QLUU Lab — SEO Content Playbook
## For the Human Team

> This doc is your operating manual for content-driven SEO. Follow it weekly and QLUU will rank for the keywords that matter.

---

## 🎯 What We're Trying to Do

1. **Rank on Google** for high-intent defense procurement keywords so DoD program managers, facility security directors, and defense contractors find QLUU when searching for counter-UAS solutions
2. **Get cited by AI** (ChatGPT, Perplexity, Google AI Overviews) when anyone asks about drone defense
3. **Build entity authority** so Google recognizes QLUU Lab as a defense technology company

---

## 📝 Blog Writing

### Where to Write
Continue using the **QLUU Blog Google Sheet** that feeds the blog:

🔗 **[QLUU Blog Sheet](https://docs.google.com/spreadsheets/d/1FoPFnDHca0zvP44gg3nBvVciuqzjP1NHoFpP6IWUwCo/edit)**

This is the single source of truth. Both the live `blog.html` page (via PapaParse) and the `build-blog.js` static generator pull from this sheet. Every post needs:

| Column | What to Put |
|--------|-------------|
| `ID` | Sequential number (next one after the last) |
| `Title` | Include target keyword. Under 60 characters |
| `Date` | Publication date (e.g., "APR 12, 2026") |
| `Tag` | One of: `THREAT INTEL`, `TECHNOLOGY`, `POLICY`, `PRODUCT` |
| `Summary` | 1-2 compelling sentences for blog cards and social previews |
| `Image URL` | Hero image URL (use dark bg, cyan accents, technical imagery) |
| `Full Article Content (HTML)` | Full HTML content with `<h2>`, `<p>`, `<ul>` tags |

### After Writing
Run the static build to make posts visible to Google:
```bash
cd c:\Users\Mike\Desktop\new-qluu-website
node build-blog.js
```
This generates individual `/blog/[id].html` files and updates `sitemap.xml`.

### Publish Cadence
**2 posts per week minimum.** Consistency beats volume.

- **Monday**: Publish post #1 → Share on LinkedIn + X
- **Thursday**: Publish post #2 → Share on LinkedIn + X

---

## 📰 What to Write About

### Category 1: Threat Intelligence (`THREAT INTEL`)
*These make QLUU the "go-to source" for drone threat news.*

**Topic Ideas:**
- Weekly drone incident roundup (Ukraine, Middle East, domestic airspace violations)
- "New Commercial Drones Being Weaponized: What Security Teams Need to Know"
- "FPV Drone Tactics: What We're Seeing in [Month] 2026"
- "Drone Swarm Incidents at Power Plants: A Growing Pattern"
- "GPS Spoofing Attacks on Civilian Drones: Defense Implications"
- "The Rise of Autonomous Drone Threats: From Hobby to National Security"

### Category 2: Technology Explainers (`TECHNOLOGY`)
*These are evergreen content that ranks for years.*

**Must-Write First:**
1. ⭐ **"What is Counter-UAS? The Complete Guide"** — This is the #1 keyword opportunity
2. ⭐ **"The C-UAS Kill Chain: Detect, Track, Identify, Mitigate"** — Framework piece
3. ⭐ **"Edge AI vs Cloud AI for Defense: Why Latency Kills"** — Differentiator

**Then:**
- "How Autonomous Drones Communicate: MAVLink Protocol Explained"
- "Swarm Intelligence: How AI Coordinates Drone Defense"
- "Kinetic vs Non-Kinetic Drone Intercept Methods"
- "What is a Sovereign AI Operating System?"
- "Why Hardware-Agnostic Matters in Counter-UAS"
- "Computer Vision for Drone Detection: How It Actually Works"

### Category 3: Industry & Policy (`POLICY`)
*These capture procurement-adjacent searches.*

- "FAA Reauthorization Act: What Changes for Counter-UAS"
- "NDAA FY2026 Counter-Drone Provisions: What Defense Companies Need to Know"
- "DoD Joint Counter-UAS Office (JCO) Explained"
- "SBIR/STTR Opportunities in Autonomous Defense for 2026"
- "Why the US Military Needs Software-Defined Defense"
- "Critical Infrastructure Protection: Federal Mandates and Compliance"

### Category 4: Product Updates (`PRODUCT`)
*Write these 1-2x per month.*

- "QLUUos Architecture Deep Dive"
- "Designing the Cyclops: Building a 200 km/h Interceptor UAV"
- "From Detection to Decision in 320 Milliseconds"
- "Field Notes: Our First Engagement Simulations"
- "How We Test Counter-UAS: Inside QLUUos Synthetic Training"

---

## ✍️ Writing Guidelines

### Every Post Should:
1. **Open with the problem** — What threat, trend, or question are you addressing?
2. **Include the target keyword** naturally in the first paragraph
3. **Be 800-1,500 words** — Google favors comprehensive content
4. **Use H2/H3 subheadings** every 200-300 words with keyword variations
5. **Link internally** — Include at least 2 links to other QLUU pages:
   - `<a href="https://qluulab.com/os.html">QLUUos</a>`
   - `<a href="https://qluulab.com/government.html">government solutions</a>`
   - `<a href="https://qluulab.com/drones.html">autonomous fleet</a>`
   - `<a href="https://qluulab.com/contact.html">contact us</a>`
6. **End with a CTA** — "Want to learn how QLUUos can protect your [infrastructure]? [Contact us](contact.html)."

### Tone
**Authoritative but accessible.** Think "Anduril blog meets War on the Rocks."
- ✅ Technical depth earns respect in defense
- ✅ Data and specifics over vague claims
- ✅ Short paragraphs, scannable structure
- ❌ Not salesy or hype-driven
- ❌ Don't say "cutting-edge" or "revolutionary"

### Image Guidelines
- Dark backgrounds with cyan accents (match QLUU brand)
- Technical imagery: radar screens, drone silhouettes, airspace maps
- Avoid stock photos of people shaking hands
- Size: at least 1200x630px (for OG social sharing)

---

## 🏛️ Entity Building — One-Time Setup Tasks

*Do these once. Update quarterly.*

### Crunchbase Profile
1. Go to [crunchbase.com/add-organization](https://www.crunchbase.com/add-organization)
2. Fill in:
   - Name: QLUU Lab, Inc.
   - HQ: California, USA
   - Founded: 2024
   - Categories: Defense, Artificial Intelligence, Drones, Counter-UAS
   - Description: "Sovereign AI platform for autonomous counter-UAS defense of critical infrastructure"
   - Website: https://qluulab.com
3. Add funding rounds, team members, board info if applicable

### LinkedIn Company Page
1. Update description (first 150 chars appear in Google):
   > "QLUU Lab builds QLUUos, a sovereign AI operating system for autonomous counter-UAS defense. Edge-deployed. Air-gapped. Hardware-agnostic. California, USA."
2. **Specialties**: Counter-UAS, Autonomous Defense, AI Operating Systems, Drone Detection, Critical Infrastructure Protection, Swarm Intelligence
3. **Post every blog article** on LinkedIn
4. Tag keywords: #CounterUAS #DroneDefense #AutonomousDefense #AIDefense

### Google Business Profile *(optional but recommended)*
1. Claim at [business.google.com](https://business.google.com)
2. Category: "Computer Security Service" or "Technology Company"
3. Service area: United States

### SAM.gov Entity
1. Verify registration at [sam.gov](https://sam.gov)
2. Ensure CAGE code is active
3. NAICS codes: 334511, 541715, 517919

### Wikipedia *(long-term, requires press coverage)*
- Not possible until third-party press coverage exists
- Milestone: Get covered in DefenseOne, Breaking Defense, or C4ISRNet
- Then create a stub article citing those sources

---

## 🔗 PR & Backlink Targets

### Publications to Pitch
| Publication | Why | How |
|------------|-----|-----|
| [Breaking Defense](https://breakingdefense.com) | Core defense tech audience | Email: tips@breakingdefense.com |
| [DefenseOne](https://defenseone.com) | DoD decision-makers read this | Pitch via LinkedIn to editors |
| [C4ISRNet](https://c4isrnet.com) | C4ISR/EW community | Apply to contributor program |
| [War on the Rocks](https://warontherocks.com) | Defense strategy community | Submit essay proposal |
| [The War Zone](https://thedrive.com/the-war-zone) | Drone/tech defense content | Email: tips@thedrive.com |
| [Small Wars Journal](https://smallwarsjournal.com) | Military practitioners | Submit article directly |
| [TechCrunch](https://techcrunch.com) | Startup/VC audience | Pitch via PressHunt |

### What to Pitch
- "Why the $5B US counter-drone market is stuck in the 2010s — and what software-first means"
- "We built an AI that makes threat decisions in 320ms. Here's what we learned."
- "The case for sovereign AI in defense: why edge beats cloud"
- "From startup to SAM.gov: how we're building defense tech differently"

### Conference Presence
Submit to speak at or exhibit:
- **AUSA Annual Meeting** (October) — Largest US Army event
- **SOF Week** (May) — Special Operations community
- **C-UAS TechWatch** — Counter-drone specific
- **DIU Vendor Days** — Defense Innovation Unit
- **Hacking 4 Defense** — University programs

---

## 📊 Weekly SEO Rhythm (15 min/week)

| Day | Task | Where |
|-----|------|-------|
| Monday | Publish blog post #1 | Google Sheets → run `node build-blog.js` |
| Monday | Share on LinkedIn + X with hashtags | LinkedIn, X |
| Thursday | Publish blog post #2 | Google Sheets → run `node build-blog.js` |
| Thursday | Share on LinkedIn + X | LinkedIn, X |
| Friday | Check Open-SEO: keyword ranks, backlinks | http://localhost:3001 |
| Friday | Log any ranking changes | Simple spreadsheet |

---

## 🚀 30-Day Launch Checklist

- [ ] Write first 3 blog posts (start with the ⭐ starred topics above)
- [ ] Run `node build-blog.js` to generate static pages
- [ ] Set up Crunchbase profile
- [ ] Update LinkedIn company page
- [ ] Claim Google Business Profile
- [ ] Sign up for DataForSEO → configure Open-SEO
- [ ] Run first keyword research in Open-SEO
- [ ] Submit sitemap to Google Search Console
- [ ] Set up 301 redirects: qluu.co → qluulab.com, qluu.website → qluulab.com
- [ ] Pitch first article to Breaking Defense or DefenseOne
