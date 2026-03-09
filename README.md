# FraudNet Sentinel  
AI‑Powered Welfare Fraud Detection and Complaint Intelligence Platform

## Overview
FraudNet Sentinel is an AI‑driven platform designed to detect corruption, fraud, and economic leakage in government welfare schemes. The system enables citizens to submit complaints through voice or text, automatically analyzes the complaint using AI techniques, and generates fraud risk insights for authorities.

The platform leverages a scalable serverless cloud architecture on AWS to process complaints, perform speech‑to‑text conversion, analyze complaint content, generate fraud risk scores, and trigger alerts for investigators. By automating complaint intelligence and fraud detection, FraudNet Sentinel helps improve transparency, reduce welfare leakage, and accelerate investigation workflows.

## Problem Statement
Government welfare schemes in India support millions of beneficiaries. However, corruption, fake beneficiaries, and misuse of public funds often result in significant economic leakage.

Citizens who face corruption frequently struggle to report complaints due to complex reporting mechanisms, lack of structured complaint analysis, and slow manual investigation processes.

There is a need for an intelligent platform that can simplify complaint submission, automatically analyze complaints for fraud indicators, and help authorities detect suspicious activities quickly and efficiently.

## Solution
FraudNet Sentinel provides an AI‑powered complaint processing and fraud detection system that automates the entire complaint lifecycle.

Citizens can submit complaints through voice recordings or text descriptions. The system converts voice complaints into text, analyzes the content using AI models to detect corruption indicators, and assigns a fraud risk score. If the complaint exceeds a predefined fraud threshold, the system generates alerts for authorities and displays insights through a monitoring dashboard.

This intelligent pipeline enables faster investigation, automated fraud detection, and data‑driven decision making for welfare monitoring.

## Key Features
Voice‑based complaint submission  
Automatic speech‑to‑text conversion  
AI‑based complaint analysis and fraud detection  
Fraud risk scoring system  
Real‑time alert generation for suspicious complaints  
Centralized monitoring dashboard for authorities  
Complaint history and investigation tracking  
Scalable serverless architecture on AWS  

## System Architecture
The platform follows a serverless cloud architecture that integrates multiple AWS services to process complaints, perform AI analysis, and store structured data.

User → React Frontend → API Gateway → AWS Lambda Backend → Amazon S3 Storage → Amazon Transcribe → Fraud Detection Model → DynamoDB Database → Alert Generation → Authority Dashboard

### Architecture Flow
1. Users submit complaints through the React frontend application.
2. The frontend communicates with backend APIs via API Gateway.
3. AWS Lambda executes the FastAPI backend logic.
4. Complaint audio and files are stored in Amazon S3.
5. Amazon Transcribe converts audio complaints into text.
6. The transcript is analyzed using an AI fraud detection model.
7. A fraud risk score is generated for each complaint.
8. Complaint data and risk scores are stored in DynamoDB.
9. Alerts are generated for high‑risk cases and displayed on the monitoring dashboard.

## AI Pipeline
Audio Complaint  
↓  
Amazon S3 Storage  
↓  
Amazon Transcribe Speech‑to‑Text  
↓  
Transcript Processing  
↓  
NLP Keyword Detection  
↓  
Fraud Detection Model  
↓  
Fraud Risk Score Generation  
↓  
Alert Creation  
↓  
Dashboard Monitoring  

The AI layer transforms unstructured complaint data into actionable fraud intelligence for investigators.

## AWS Services Used
AWS Amplify – Frontend hosting and deployment  
Amazon API Gateway – API management and routing  
AWS Lambda – Serverless backend execution  
Amazon S3 – Storage for audio files, reports, transcripts, and processed data  
Amazon DynamoDB – NoSQL database for complaints, beneficiaries, risk scores, and alerts  
Amazon Transcribe – Speech‑to‑text conversion for voice complaints  
Amazon Cognito – User authentication and access control  
Amazon CloudWatch – System monitoring and logging  

## AI Expansion Capabilities
The architecture is designed to easily integrate advanced AI services for future enhancements.

Amazon SageMaker can be used to train and deploy large‑scale fraud detection models using historical complaint data.

Amazon Neptune can be integrated for graph‑based fraud network detection to identify relationships between beneficiaries, bank accounts, and addresses.

Amazon Bedrock can provide generative AI capabilities such as automated investigation summaries and AI‑generated fraud insights for authorities.

## Technology Stack
Frontend  
React  
Vite  
Tailwind CSS  
Axios  

Backend  
FastAPI  
Python  
Mangum (Lambda adapter)

Database  
Amazon DynamoDB  

AI and Cloud Services  
Amazon Transcribe  
Fraud Detection Model (Scikit‑learn based)  

Infrastructure  
AWS Amplify  
API Gateway  
AWS Lambda  
Amazon S3  
Amazon Cognito  
Amazon CloudWatch  

## Prototype Performance
Average complaint processing time: 3‑6 seconds  
Speech‑to‑text accuracy: approximately 90‑95 percent for clear audio  
Fraud detection model response time: less than 1 second  
Alert generation: real‑time  
System scalability: capable of processing thousands of complaints per day using serverless infrastructure  
Estimated system availability: approximately 99.9 percent  

## Video Demonstration 

https://github.com/user-attachments/assets/e0ea5b89-a54f-4d58-9f56-6bcc8a2ad2b6


## Future Enhancements
Integration of advanced fraud detection models using Amazon SageMaker  
Graph‑based fraud network detection using Amazon Neptune  
Generative AI investigation insights using Amazon Bedrock  
Support for multilingual complaint processing across regional languages  
Mobile application for citizen complaint reporting  
Predictive analytics for identifying high‑risk districts and welfare schemes  

## Demo Access
Live Application  
Frontend deployed using AWS Amplify.

Demo Login Credentials  
Email: demo40016@gmail.com  
Password: Demo@12345

## Repository Structure
backend  
Contains FastAPI backend, AWS Lambda handlers, AI processing pipeline, and service integrations.

frontend  
Contains the React‑based dashboard interface used by citizens and authorities.

start.sh / start.bat  
Scripts to run the project locally.

## Impact
FraudNet Sentinel helps governments improve transparency and accountability in welfare systems by automating complaint analysis and detecting corruption patterns. The platform enables authorities to prioritize high‑risk cases, reduce manual investigation workload, and prevent economic leakage in public welfare programs.

## License
This project is developed as part of the AWS AI for Bharat Hackathon and is intended for educational and research purposes.
