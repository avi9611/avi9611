<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=260&color=0:0B1220,40:1E3A8A,100:38BDF8&text=Avinash%20Neralakatte&fontSize=44&fontColor=EAF2FF&fontAlignY=34&desc=Full-Stack%20Engineer%20%E2%80%A2%20CRM%20and%20ERP%20%E2%80%A2%20FastAPI%20and%20Next.js&descSize=17&descAlignY=58" alt="Avinash Neralakatte — Full-Stack Engineer" />
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1400&color=93C5FD&center=true&vCenter=true&width=980&lines=Full-Stack+Engineer+%40+Hybrid+Interactive+%C2%B7+Kochi;Eight+production+products+shipped+in+nine+months;Healthcare+%C2%B7+Hospitality+%C2%B7+Construction+%C2%B7+Calibration+%C2%B7+HR;I+wrote+the+templates+and+conventions+my+team+builds+on" alt="Full-Stack Engineer at Hybrid Interactive. Eight production products shipped in nine months." />
</p>

<p align="center">
  <a href="https://avi9611.github.io">
    <img src="https://img.shields.io/badge/Portfolio-avi9611.github.io-0F172A?style=for-the-badge&logo=firefoxbrowser&logoColor=white" alt="Portfolio" />
  </a>
  <a href="https://www.linkedin.com/in/avinash-n-dev/">
    <img src="https://img.shields.io/badge/LinkedIn-avinash--n--dev-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
  <a href="https://avi9611.github.io/avinashresume.pdf">
    <img src="https://img.shields.io/badge/CV-Download%20PDF-166534?style=for-the-badge&logo=readme&logoColor=white" alt="Download CV" />
  </a>
  <a href="mailto:avinashpoojary651@gmail.com">
    <img src="https://img.shields.io/badge/Email-Get%20in%20touch-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" />
  </a>
  <img src="https://komarev.com/ghpvc/?username=avi9611&label=Profile%20views&color=1E3A8A&style=for-the-badge" alt="Profile views" />
</p>

---

## About

I build **line-of-business software** — the CRM, ERP, hospital and HR systems a
company's daily operations actually depend on. In nine months at Hybrid
Interactive I have shipped **eight production products** across healthcare,
hospitality, construction, calibration, sales and HR.

The hard parts of this work are rarely the framework. They are the tenancy model,
the audit trail, the state machine that decides what a document is allowed to
become next, and whether the person who picks the code up after me can still read
it. My largest system is a lead-to-cash CRM for a UAE medical-equipment
calibration laboratory: **18 business modules**, multi-branch, audit-backed, built
to contractual SLA targets. I wrote **98% of both repositories**.

On the AI side I integrate LLM features into real product surfaces — **Pydantic AI**
for typed agent behaviour, **RAG pipelines** over client data, and direct API calls
where a full agent framework would be overkill. I also work agentically day to
day with **Claude Code, Codex and Copilot**, with deliberate judgement about where
a model speeds up real progress and where it just adds noise.

---

## What I build

| Area | Focus |
| :--- | :--- |
| **Backend** | FastAPI · async SQLAlchemy 2.0 · PostgreSQL · Redis · Celery · Alembic |
| **Frontend** | Next.js App Router · React 19 · TypeScript · TanStack Query · Tailwind |
| **Architecture** | Modular monoliths · multi-tenancy · RBAC · append-only audit trails |
| **Reliability** | Background workers · caching · Prometheus · structured logging |
| **AI in product** | Pydantic AI · RAG pipelines · LLM APIs in real workflows |
| **Practice** | Written standards · architecture decision records · docs that carry a date |

---

## Standards I wrote

Client work is what I ship. These are what my team builds on.

- **[Next.js Frontend Template](https://github.com/hybridinteract/nextjs-template)** — Built and documented on my own. 143 files: BFF cookie auth so tokens never reach JavaScript, RBAC gating navigation and components, TanStack Query, Vitest and Playwright. Documented in **17 numbered rule guides** plus an architecture guide, so the reasoning survives me.
- **Backend Conventions Kit** — A portable folder you copy into a new backend on day one. 17 concern guides covering permissions, migrations, caching, tenancy, timezones, money and state machines, plus a checker that fails the commit when a doc goes stale. *Every rule in it was paid for once already, by a bug that shipped.*
- **[FastAPI Backend Template](https://github.com/hybridinteract/fastapi-template)** — Co-designed. Modular monolith by feature domain. Routes hold no business logic, services own the transaction boundary, data access never commits.
- **[Engineering Standards @ Hybrid Interactive](https://engineering.hybridinteractive.in/)** — Contributed to the company's public documentation hub.

---

## Core stack

<p align="center">
  <img src="https://skillicons.dev/icons?i=fastapi,python,nextjs,react,ts,postgres,redis,docker,tailwind,githubactions,git,linux&perline=6" alt="FastAPI, Python, Next.js, React, TypeScript, PostgreSQL, Redis, Docker, Tailwind, GitHub Actions, Git, Linux" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Backend-FastAPI%20%C2%B7%20SQLAlchemy%20%C2%B7%20Celery-0F172A?style=for-the-badge&labelColor=111827&color=1E3A8A" alt="Backend" />
  <img src="https://img.shields.io/badge/Frontend-Next.js%20%C2%B7%20React%20%C2%B7%20TypeScript-0F172A?style=for-the-badge&labelColor=111827&color=1D4ED8" alt="Frontend" />
  <img src="https://img.shields.io/badge/Data-PostgreSQL%20%C2%B7%20Redis%20%C2%B7%20Docker-0F172A?style=for-the-badge&labelColor=111827&color=2563EB" alt="Data and infrastructure" />
  <img src="https://img.shields.io/badge/AI-Pydantic%20AI%20%C2%B7%20RAG%20%C2%B7%20LLM%20APIs-0F172A?style=for-the-badge&labelColor=111827&color=38BDF8" alt="AI" />
</p>

---

## Selected personal work

| Project | What it is | Stack |
| :--- | :--- | :--- |
| **[Nadisa Solutions](https://www.nadisasolutions.com/)** | Live career-guidance platform for chemistry professionals. Built solo. | Next.js 16 · React 19 · Firebase |
| **[Code Eval AI](https://github.com/avi9611/code-eval-ai)** | AI-assisted code and interface review workspace with structured scoring. | React · Node · PostgreSQL · Gemini |
| **[ClickTalk](https://github.com/avi9611/Click-Talk-MERN-App)** | Realtime chat with presence and secure auth. | MERN · Socket.IO · Zustand |
| **[BookStore](https://github.com/avi9611/book-store-nextjs)** | Catalogue and inventory interface. | Next.js · PostgreSQL · Drizzle |

More, including the client work, at **[avi9611.github.io](https://avi9611.github.io)**.

---

## Practice

<p align="center">
  <img src="https://img.shields.io/badge/Microsoft%20Certified-Azure%20Fundamentals-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white" alt="Microsoft Certified: Azure Fundamentals" />
  <img src="https://img.shields.io/badge/MCA-VTU%20%C2%B7%20CGPA%208.85-1E3A8A?style=for-the-badge&logo=googlescholar&logoColor=white" alt="MCA, VTU, CGPA 8.85" />
</p>

<p align="center">
  <a href="https://leetcode.com/u/avinash516/">
    <img src="https://leetcard.jacoblin.cool/avinash516?theme=dark&font=Fira%20Code&ext=heatmap" alt="LeetCode stats" />
  </a>
</p>

---

<p align="center">
  <em>Build for the person debugging this at 2am, not the person reading it today.</em>
  <br/>
  <sub><strong>Open to conversations about backend architecture and product delivery.</strong></sub>
</p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:38BDF8,50:1E3A8A,100:0B1220&section=footer" alt="" />
</p>
