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
    \small Cloud Engineer $|$ AWS Certified Cloud Practitioner \\ \vspace{2pt}
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
        \resumeItem{Provisioned and managed core AWS resources -- EC2, S3, IAM, VPC, RDS, DynamoDB, Aurora, and Lambda -- across hands-on cloud lab environments.}
        \resumeItem{Designed, subnetted, and troubleshot VPC networks (public/private subnets, routing tables, NAT gateways) and configured monitoring pipelines using CloudWatch and CloudTrail.}
        \resumeItem{Automated infrastructure provisioning with AWS CloudFormation templates (JSON/YAML) and EC2 launch templates; deployed static websites on Amazon S3.}
        \resumeItem{Administered Linux-based EC2 instances via Bash shell scripting, managed IAM security policies and SSH access, and applied AWS Well-Architected Framework principles.}
      \resumeItemListEnd
  \resumeSubHeadingListEnd

%-----------PROJECTS-----------
\section{Projects}
  \resumeSubHeadingListStart
    \resumeProjectHeading
      {\textbf{Serverless Event-Driven CloudOps Pipeline} $|$ \emph{AWS (Lambda, S3, DynamoDB, SNS, SQS), Terraform, Python}}{}
      \resumeItemListStart
        \resumeItem{Architected an event-driven serverless ingestion pipeline on AWS using S3 event triggers, Dockerized Lambda microservices (ECR), and DynamoDB for automated issue intake and classification.}
        \resumeItem{Automated 100\% of infrastructure provisioning using Terraform (IaC) with remote S3 state management, least-privilege IAM roles, and date-partitioned S3 storage (\texttt{processed/YYYY/MM/DD/}).}
        \resumeItem{Implemented multi-channel alerting for high-severity incidents using an Amazon SNS topic fanning out to an SQS queue backed by a Dead-Letter Queue (DLQ) for zero alert loss.}
        \resumeItem{Deployed a containerized Flask web portal on Render featuring live ticket submission, an asynchronous processing countdown, and real-time DynamoDB operational feed synchronization.}
      \resumeItemListEnd

    \resumeProjectHeading
      {\textbf{YouTube Analytics Platform} $|$ \emph{Python, FastAPI, AWS Cognito, DynamoDB, SQLite, Google Gemini, REST APIs}}{}
      \resumeItemListStart
        \resumeItem{Developed and deployed a FastAPI backend integrating YouTube Data API v3 to retrieve, process, and analyze real-time channel analytics.}
        \resumeItem{Integrated AWS Cognito with Google Sign-In for secure, JWT-based authorization on protected API endpoints.}
        \resumeItem{Designed a cloud-backed architecture using DynamoDB for persistent, user-specific chat history and analytics data.}
        \resumeItem{Implemented intelligent caching with SQLite, cutting redundant YouTube API requests by approximately 80\% and improving responsiveness.}
        \resumeItem{Built an AI-powered analytics assistant using Google Gemini with persistent conversational context via DynamoDB.}
      \resumeItemListEnd
  \resumeSubHeadingListEnd

%-----------TECHNICAL SKILLS-----------
\section{Technical Skills}
 \begin{itemize}[leftmargin=0.15in, label={}, itemsep=1.5pt, parsep=0pt]
    \small{\item{
     \textbf{Cloud (AWS):} Lambda, S3, DynamoDB, EC2, IAM, VPC, RDS, SNS, SQS, ECR, CloudFormation, CloudWatch, CloudTrail, Route 53 \\
     \textbf{Infrastructure as Code \& DevOps:} Terraform, Docker, GitHub Actions (CI/CD), Git, GitHub, JSON/YAML \\
     \textbf{Programming \& Scripting:} Python (Boto3), SQL, Bash Shell Scripting \\
     \textbf{Networking \& Systems:} VPC Design, Subnetting, Routing Tables, Security Groups, Linux Administration \\
     \textbf{Backend \& Databases:} FastAPI, Flask, REST APIs, PostgreSQL, MySQL, SQLite
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
