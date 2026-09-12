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
    \small Data Engineer $|$ Python $|$ SQL $|$ AWS Data Pipelines \\ \vspace{2pt}
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
      {Cloud Computing Trainee -- Tata STRIVE (AWS Program)}{Jan 2026 -- Apr 2026}
      {12-week intensive AWS cloud training program}{}
      \resumeItemListStart
        \resumeItem{Provisioned and managed AWS resources including EC2, S3, IAM, VPC, RDS, and CloudWatch while working in hands-on cloud lab environments.}
        \resumeItem{Configured Linux-based EC2 instances, implemented IAM security policies, managed SSH access, and secured cloud infrastructure.}
        \resumeItem{Performed deployment, monitoring, logging, and troubleshooting activities across simulated production cloud environments.}
      \resumeItemListEnd
  \resumeSubHeadingListEnd

%-----------PROJECTS-----------
\section{Projects}
  \resumeSubHeadingListStart
    \resumeProjectHeading
      {\textbf{Event-Driven Serverless ETL Pipeline} $|$ \emph{AWS (S3, Lambda, DynamoDB), Apache Airflow, Python, SQS, DLQ}}{}
      \resumeItemListStart
        \resumeItem{Designed an asynchronous event-driven ETL pipeline on AWS using S3 object triggers and containerized Lambda functions to extract, clean, and enrich unstructured text records.}
        \resumeItem{Implemented date-partitioned raw-to-processed data archiving in Amazon S3 (\texttt{processed/YYYY/MM/DD/}) alongside sub-second record persistence into Amazon DynamoDB NoSQL tables.}
        \resumeItem{Configured SQS Dead-Letter Queues (DLQ) with retry policies (\texttt{maxReceiveCount=3}) to quarantine malformed schemas and prevent data loss during ingestion spikes.}
        \resumeItem{Authored an Apache Airflow DAG utilizing the TaskFlow API (\texttt{@dag}, \texttt{@task}) to automate batch ETL reconciliation, error handling callbacks, and database loads.}
      \resumeItemListEnd

    \resumeProjectHeading
      {\textbf{Stock Market Analytics Platform} $|$ \emph{PostgreSQL, SQL, Database Design, Data Modeling}}{}
      \resumeItemListStart
        \resumeItem{Designed a normalized PostgreSQL database schema for storing and managing historical NIFTY 500 market data.}
        \resumeItem{Developed advanced SQL queries using joins, aggregations, Common Table Expressions (CTEs), and window functions to analyze sector performance, trading activity, and stock rankings.}
        \resumeItem{Optimized database performance through indexing and efficient query design, enabling faster analytical queries on large financial datasets.}
        \resumeItem{Built an interactive analytics platform for exploring historical market trends, sector performance, and stock-level insights.}
      \resumeItemListEnd
  \resumeSubHeadingListEnd

%-----------TECHNICAL SKILLS-----------
\section{Technical Skills}
 \begin{itemize}[leftmargin=0.15in, label={}, itemsep=1.5pt, parsep=0pt]
    \small{\item{
     \textbf{Data Engineering:} ETL/ELT Pipelines, Event-Driven Processing, Data Partitioning, Schema Validation, Data Modeling \\
     \textbf{Data Technologies \& Orchestration:} Apache Airflow (TaskFlow API, DAGs), Amazon S3, Amazon DynamoDB, PostgreSQL, SQLite \\
     \textbf{Programming \& Querying:} Python (Boto3, Pandas basics), Advanced SQL (Window Functions, CTEs, Aggregations) \\
     \textbf{Cloud \& Infrastructure:} AWS (Lambda, S3, DynamoDB, SQS, SNS, CloudWatch), Terraform basics, Docker \\
     \textbf{Tools \& Practices:} Git, GitHub, Linux Shell, Unit Testing (\texttt{pytest}), JSON/YAML Formats
    }}
 \end{itemize}

%-----------CERTIFICATIONS-----------
\section{Certifications}
 \begin{itemize}[leftmargin=0.15in, label={}, itemsep=1.5pt, parsep=0pt]
    \small{\item{
     $\bullet$ \textbf{AWS Certified Cloud Practitioner} -- AWS $|$ \textbf{Python Developer Certificate} -- LetsUpgrade \\
     $\bullet$ \textbf{Data Science \& Analytics} -- HP LIFE $|$ \textbf{AI for Beginners} -- HP LIFE
    }}
 \end{itemize}

\end{document}
