\documentclass[letterpaper,10pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\input{glyphtounicode}

% Font options
\usepackage[default]{sourcesanspro}
\urlstyle{same}

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Adjust margins
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% Sections formatting
\titleformat{\section}{
  \vspace{-6pt}\scshape\raggedright\large\bfseries
}{}{0em}{}[\color{black}\titlerule \vspace{-4pt}]

% Ensure that generate pdf is machine readable/ATS parsable
\pdfgentounicode=1

% Custom commands
\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-1pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-6pt}
}

\newcommand{\resumeProjectHeading}[2]{
  \vspace{-1pt}\item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-6pt}
}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}[leftmargin=0.15in, itemsep=1.5pt, parsep=0pt]}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-4pt}}

\begin{document}

%----------HEADING----------
\begin{center}
    \textbf{\Huge \scshape Aakashdeep Dhall} \\ \vspace{2pt}
    \small DevOps \& Cloud Engineer $|$ CI/CD $|$ Kubernetes $|$ Terraform \\ \vspace{2pt}
    \small +91 9310466547 $|$ \href{mailto:aakashdeep14122004@gmail.com}{\underline{aakashdeep14122004@gmail.com}} $|$ 
    \href{https://linkedin.com/in/aakashdeep-dhall}{\underline{LinkedIn}} $|$
    \href{https://github.com/pogg144p}{\underline{GitHub}} $|$
    Delhi, India
\end{center}

%-----------EDUCATION-----------
\section{Education}
  \resumeSubHeadingListStart
    \resumeSubheading
      {Maharishi Dayanand University}{2022 -- 2026}
      {B.Tech -- Computer Science Engineering}{Rohtak, India}
    \resumeSubheading
      {Vandana International Sr. Sec. School}{2021 -- 2022}
      {Senior Secondary (Class XII)}{Delhi, India}
  \resumeSubHeadingListEnd

%-----------EXPERIENCE-----------
\section{Experience}
  \resumeSubHeadingListStart
    \resumeSubheading
      {Cloud Computing Student Trainee -- Tata STRIVE (AWS re/Start Program)}{Jan 2026 -- Apr 2026}
      {12-week intensive AWS cloud training program}{}
      \resumeItemListStart
        \resumeItem{Provisioned and managed AWS infrastructure including EC2, S3, IAM, VPC, RDS, and CloudWatch in hands-on cloud lab environments.}
        \resumeItem{Configured Linux-based EC2 instances, implemented IAM security policies, managed SSH key access, and secured cloud environments.}
        \resumeItem{Performed automated deployment, monitoring, log analysis, and troubleshooting across simulated production cloud setups.}
      \resumeItemListEnd
  \resumeSubHeadingListEnd

%-----------PROJECTS-----------
\section{Projects}
  \resumeSubHeadingListStart
    \resumeProjectHeading
      {\textbf{CloudOps Automation \& Serverless Platform} $|$ \emph{Terraform, Docker, Kubernetes, GitHub Actions, AWS, Prometheus}}{}
      \resumeItemListStart
        \resumeItem{Engineered an end-to-end GitOps CI/CD pipeline using GitHub Actions to automate linting (\texttt{flake8}), unit testing with mocked AWS SDK calls (\texttt{pytest}), and multi-stage Docker builds pushed to Amazon ECR.}
        \resumeItem{Provisioned AWS infrastructure (S3, DynamoDB, Lambda, SNS, SQS) via modular Terraform code, enforcing remote S3 state locking and least-privilege IAM security policies.}
        \resumeItem{Authored production Kubernetes manifests (Deployments, Services, ConfigMaps, Secrets, Ingress, HPA) featuring zero-downtime rolling updates (\texttt{maxSurge=1}) and automated horizontal scaling.}
        \resumeItem{Configured Prometheus and Alertmanager monitoring configurations with custom PromQL alert rules for tracking pipeline latency, error rates, and critical bug threshold spikes.}
        \resumeItem{Developed Ansible automation playbooks to streamline node provisioning, Docker installation, firewall rules (UFW), and Nginx reverse proxy configurations.}
      \resumeItemListEnd

    \resumeProjectHeading
      {\textbf{YouTube Analytics Platform} $|$ \emph{Python, FastAPI, Docker, AWS Cognito, DynamoDB, REST APIs}}{}
      \resumeItemListStart
        \resumeItem{Developed a modular FastAPI backend delivering real-time YouTube metrics, containerized with Docker for consistent multi-environment deployment.}
        \resumeItem{Configured AWS Cognito user pools and JWT-based authentication for securing API routes against unauthorized traffic.}
        \resumeItem{Implemented NoSQL persistence using DynamoDB to store user telemetry, conversation history, and analytics state.}
        \resumeItem{Implemented caching layers to reduce upstream API consumption by 80\%, preventing rate-limiting under high query volume.}
      \resumeItemListEnd
  \resumeSubHeadingListEnd

%-----------TECHNICAL SKILLS-----------
\section{Technical Skills}
 \begin{itemize}[leftmargin=0.15in, label={}, itemsep=1.5pt, parsep=0pt]
    \small{\item{
     \textbf{DevOps \& CI/CD:} GitHub Actions, GitOps, Docker, Docker Compose, Linux Administration, Bash Scripting \\
     \textbf{Orchestration \& Config:} Kubernetes (Deployments, HPA, Ingress, Probes), Ansible Playbooks \\
     \textbf{Infrastructure as Code (IaC):} Terraform (HCL), Remote State Backend (S3), AWS CloudFormation \\
     \textbf{Cloud (AWS):} Lambda, S3, DynamoDB, ECR, SQS, SNS, EC2, IAM, CloudWatch, VPC \\
     \textbf{Monitoring \& Observability:} Prometheus, Alertmanager, PromQL, CloudWatch Metrics \\
     \textbf{Languages \& Frameworks:} Python (Boto3, Pytest), Flask, FastAPI, SQL, JSON/YAML
    }}
 \end{itemize}

%-----------CERTIFICATIONS-----------
\section{Certifications}
 \begin{itemize}[leftmargin=0.15in, label={}, itemsep=1.5pt, parsep=0pt]
    \small{\item{
     $\bullet$ \textbf{AWS Certified Cloud Practitioner} -- Amazon Web Services \\
     $\bullet$ \textbf{Python Developer Certificate} -- LetsUpgrade \\
     $\bullet$ \textbf{Data Science \& Analytics} -- HP LIFE $|$ \textbf{AI for Beginners} -- HP LIFE
    }}
 \end{itemize}

\end{document}
