# FraudNet Sentinel - Requirements Specification

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. System Overview](#2-system-overview)
- [3. Functional Requirements](#3-functional-requirements)
- [4. Non-Functional Requirements](#4-non-functional-requirements)
- [5. User Requirements](#5-user-requirements)
- [6. System Requirements](#6-system-requirements)
- [7. Data Requirements](#7-data-requirements)
- [8. Integration Requirements](#8-integration-requirements)
- [9. Security Requirements](#9-security-requirements)
- [10. Compliance Requirements](#10-compliance-requirements)

---

## 1. Introduction

### 1.1 Purpose
FraudNet Sentinel is an AI-powered fraud detection and economic leakage prevention system designed for government welfare schemes. The system identifies duplicate beneficiaries, ghost beneficiaries, fraudulent activities, and corruption in benefit distribution programs.

### 1.2 Scope
The system provides:
- Real-time fraud detection using AI/ML models
- Complaint management with audio evidence
- Risk assessment and scoring
- Fraud network analysis
- Analytics and reporting dashboard
- Alert monitoring and notification system

### 1.3 Definitions and Acronyms
- **ELD**: Economic Leakage Detection
- **API**: Application Programming Interface
- **ML**: Machine Learning
- **NLP**: Natural Language Processing
- **S3**: Amazon Simple Storage Service
- **DynamoDB**: Amazon NoSQL Database Service
- **JWT**: JSON Web Token

### 1.4 References
- AWS Lambda Documentation
- FastAPI Documentation
- React Documentation
- DynamoDB Best Practices

---

## 2. System Overview

### 2.1 System Context
FraudNet Sentinel operates as a cloud-based SaaS platform deployed on AWS infrastructure, serving government agencies responsible for welfare scheme administration.

### 2.2 System Architecture
- **Frontend**: React-based web application
- **Backend**: FastAPI REST API on AWS Lambda
- **Database**: DynamoDB for NoSQL data storage
- **Storage**: S3 for audio/document storage
- **AI/ML**: Custom fraud detection models

### 2.3 User Roles
1. **System Administrator**: Full system access and configuration
2. **Investigator**: Review complaints and conduct investigations
3. **Analyst**: View analytics and generate reports
4. **Public User**: Submit complaints (authenticated or anonymous)

---

## 3. Functional Requirements

### 3.1 Authentication & Authorization

#### FR-AUTH-001: User Login
- **Priority**: High
- **Description**: Users must authenticate using email and password
- **Acceptance Criteria**:
  - Valid credentials grant access with JWT token
  - Invalid credentials show error message
  - Token expires after 24 hours
  - Refresh token mechanism available

#### FR-AUTH-002: Logout
- **Priority**: High
- **Description**: Users can logout and clear session
- **Acceptance Criteria**:
  - Logout clears all tokens from storage
  - User redirected to login page
  - Protected routes become inaccessible

#### FR-AUTH-003: Protected Routes
- **Priority**: High
- **Description**: Sensitive pages require authentication
- **Acceptance Criteria**:
  - Unauthenticated users redirected to login
  - Token validation on each request
  - Expired tokens trigger re-authentication

---

### 3.2 Beneficiary Management

#### FR-BEN-001: Register Beneficiary
- **Priority**: High
- **Description**: System registers new beneficiaries with validation
- **Acceptance Criteria**:
  - Capture: name, DOB, gender, address, phone, bank account, district, scheme, amount
  - Validate Aadhaar format (12 digits)
  - Hash bank account for privacy
  - Generate unique beneficiary ID (BEN-XXXXXXXXX)
  - Perform duplicate detection on registration

#### FR-BEN-002: View Beneficiary List
- **Priority**: High
- **Description**: Display all registered beneficiaries
- **Acceptance Criteria**:
  - Show beneficiary ID, name, district, risk score, status
  - Support pagination (10 items per page)
  - Filter by district, risk category
  - Search by ID or name

#### FR-BEN-003: View Beneficiary Details
- **Priority**: Medium
- **Description**: Display detailed beneficiary information
- **Acceptance Criteria**:
  - Show all beneficiary attributes
  - Display risk assessment details
  - Show associated complaints
  - Display fraud network connections

#### FR-BEN-004: Risk Assessment
- **Priority**: High
- **Description**: Calculate and display risk scores
- **Acceptance Criteria**:
  - Risk score: 0.0 to 1.0
  - Risk categories: Low (<0.4), Medium (0.4-0.7), High (0.7-0.9), Critical (>0.9)
  - Factors: duplicate score, anomaly score, network centrality, complaint severity
  - Update risk score on new data

#### FR-BEN-005: Fraud Network Detection
- **Priority**: Medium
- **Description**: Identify connected beneficiaries in fraud networks
- **Acceptance Criteria**:
  - Detect shared resources (bank account, phone, address)
  - Calculate network centrality scores
  - Visualize network graph
  - Support depth parameter (1-5 levels)

---

### 3.3 Complaint Management

#### FR-COMP-001: Submit Complaint
- **Priority**: High
- **Description**: Users can submit fraud complaints
- **Acceptance Criteria**:
  - Complaint types: duplicate_beneficiary, ghost_beneficiary, fraud, bribery, wrong_amount
  - Required: complaint_type, description, district
  - Optional: beneficiary_id, block, audio, report, submitter details
  - Support anonymous submissions
  - Generate unique complaint ID (CMP-XXXXXXXX)
  - Auto-generate beneficiary_id if missing (BEN-XXXXXX)

#### FR-COMP-002: Upload Audio Evidence
- **Priority**: Medium
- **Description**: Upload audio recordings as evidence
- **Acceptance Criteria**:
  - Supported formats: MP3, WAV, M4A, OGG
  - Max file size: 50MB
  - Upload to S3 bucket
  - Return S3 URL
  - Trigger transcription job (AWS Transcribe)

#### FR-COMP-003: Upload Document Evidence
- **Priority**: Medium
- **Description**: Upload supporting documents
- **Acceptance Criteria**:
  - Supported formats: PDF, DOC, DOCX, JPG, PNG
  - Max file size: 10MB
  - Upload to S3 bucket
  - Return S3 URL

#### FR-COMP-004: View Complaints
- **Priority**: High
- **Description**: Display all complaints with filtering
- **Acceptance Criteria**:
  - Show complaint ID, beneficiary ID, type, status, date, fraud score
  - Filter by: status, fraud score, date range
  - Search by: complaint ID, beneficiary ID, description
  - Pagination support
  - Sort by date (newest first)

#### FR-COMP-005: View Complaint Details
- **Priority**: High
- **Description**: Display detailed complaint information
- **Acceptance Criteria**:
  - Show all complaint attributes
  - Display audio player for audio evidence
  - Show transcript if available
  - Display document preview/download link
  - Show fraud score and analysis

#### FR-COMP-006: Audio Playback
- **Priority**: Medium
- **Description**: Play audio evidence in browser
- **Acceptance Criteria**:
  - HTML5 audio player
  - Controls: play, pause, seek, volume, skip (±10s)
  - Display duration and current time
  - Progress bar with seek functionality

#### FR-COMP-007: Update Complaint Status
- **Priority**: Medium
- **Description**: Change complaint status during investigation
- **Acceptance Criteria**:
  - Statuses: submitted, investigating, resolved, rejected
  - Status change logged with timestamp
  - Notification sent on status change

#### FR-COMP-008: NLP Analysis
- **Priority**: Medium
- **Description**: Analyze complaint text using NLP
- **Acceptance Criteria**:
  - Extract urgency score (0.0-1.0)
  - Sentiment analysis (-1.0 to 1.0)
  - Predict complaint type
  - Extract beneficiary ID from text if present

---

### 3.4 Alert Management

#### FR-ALERT-001: Generate Alerts
- **Priority**: High
- **Description**: Automatically create alerts for high-risk cases
- **Acceptance Criteria**:
  - Trigger on: risk score ≥ 0.6, duplicate detection, fraud network detection
  - Severity levels: low, medium, high, critical
  - Alert types: high_risk_beneficiary, duplicate_detected, fraud_network, suspicious_activity
  - Generate unique alert ID (ALT-XXXXXXXXX)

#### FR-ALERT-002: View Alerts
- **Priority**: High
- **Description**: Display all active alerts
- **Acceptance Criteria**:
  - Show alert ID, type, severity, beneficiary ID, risk score, date
  - Filter by severity
  - Sort by date (newest first)
  - Show alert count by severity

#### FR-ALERT-003: View Alert Details
- **Priority**: Medium
- **Description**: Display detailed alert information
- **Acceptance Criteria**:
  - Show all alert attributes
  - Display associated beneficiary details
  - Show risk factors and explanation
  - Provide action recommendations

#### FR-ALERT-004: Acknowledge Alert
- **Priority**: Medium
- **Description**: Mark alert as acknowledged
- **Acceptance Criteria**:
  - Change status to acknowledged
  - Record acknowledger and timestamp
  - Alert remains visible but marked

---

### 3.5 Analytics & Reporting

#### FR-ANALYTICS-001: Dashboard Summary
- **Priority**: High
- **Description**: Display key metrics on dashboard
- **Acceptance Criteria**:
  - Total beneficiaries count
  - High-risk cases count
  - Active alerts count
  - Total complaints count
  - Total disbursement amount
  - Potential leakage amount
  - Duplicate count
  - Flagged count

#### FR-ANALYTICS-002: District Risk Analysis
- **Priority**: High
- **Description**: Show risk metrics by district
- **Acceptance Criteria**:
  - Average risk score per district
  - Risk category distribution
  - Total beneficiaries per district
  - High-risk count per district
  - Total amount per district
  - Sort by risk score (descending)

#### FR-ANALYTICS-003: Fraud Networks
- **Priority**: Medium
- **Description**: Display detected fraud networks
- **Acceptance Criteria**:
  - Network count
  - Beneficiaries involved count
  - Pattern types: shared_resources, connected_clusters, high_centrality
  - Network size and risk score
  - Shared resource details

#### FR-ANALYTICS-004: Trends Analysis
- **Priority**: Medium
- **Description**: Show leakage and detection trends
- **Acceptance Criteria**:
  - Leakage trend over time (line chart)
  - Detection trend over time (line chart)
  - Trend direction: improving/worsening
  - Percentage change calculation
  - Date range: last 6 months

#### FR-ANALYTICS-005: Risk Distribution
- **Priority**: Medium
- **Description**: Visualize risk category distribution
- **Acceptance Criteria**:
  - Pie chart showing critical, high, medium, low
  - Percentage and count for each category
  - Interactive chart with tooltips

---

### 3.6 Dashboard Features

#### FR-DASH-001: Real-time Data
- **Priority**: High
- **Description**: Dashboard displays real-time data
- **Acceptance Criteria**:
  - Auto-refresh every 5 minutes
  - Manual refresh button
  - Loading states during data fetch
  - Error handling with retry option

#### FR-DASH-002: Recent Activity
- **Priority**: Medium
- **Description**: Show recent complaints and alerts
- **Acceptance Criteria**:
  - Display last 5 complaints
  - Display last 5 high-risk alerts
  - Show status badges
  - Link to detail pages

#### FR-DASH-003: Charts & Visualizations
- **Priority**: Medium
- **Description**: Interactive charts for data visualization
- **Acceptance Criteria**:
  - Pie chart for risk distribution
  - Line chart for leakage trends
  - Bar chart for district comparison
  - Tooltips on hover
  - Responsive design

---

## 4. Non-Functional Requirements

### 4.1 Performance Requirements

#### NFR-PERF-001: Response Time
- **Priority**: High
- **Requirement**: API responses within 2 seconds for 95% of requests
- **Measurement**: CloudWatch metrics

#### NFR-PERF-002: Page Load Time
- **Priority**: High
- **Requirement**: Initial page load within 3 seconds
- **Measurement**: Lighthouse performance score ≥ 80

#### NFR-PERF-003: Concurrent Users
- **Priority**: Medium
- **Requirement**: Support 100 concurrent users
- **Measurement**: Load testing with JMeter

#### NFR-PERF-004: Database Query Time
- **Priority**: High
- **Requirement**: DynamoDB queries within 100ms
- **Measurement**: X-Ray tracing

---

### 4.2 Scalability Requirements

#### NFR-SCALE-001: Horizontal Scaling
- **Priority**: High
- **Requirement**: Auto-scale Lambda functions based on load
- **Implementation**: AWS Lambda auto-scaling

#### NFR-SCALE-002: Data Volume
- **Priority**: High
- **Requirement**: Handle 1 million beneficiaries
- **Implementation**: DynamoDB with GSI

#### NFR-SCALE-003: File Storage
- **Priority**: Medium
- **Requirement**: Store up to 10TB of audio/documents
- **Implementation**: S3 with lifecycle policies

---

### 4.3 Availability Requirements

#### NFR-AVAIL-001: Uptime
- **Priority**: High
- **Requirement**: 99.9% uptime (8.76 hours downtime/year)
- **Measurement**: CloudWatch alarms

#### NFR-AVAIL-002: Disaster Recovery
- **Priority**: High
- **Requirement**: RPO: 1 hour, RTO: 4 hours
- **Implementation**: Multi-AZ deployment, automated backups

#### NFR-AVAIL-003: Backup
- **Priority**: High
- **Requirement**: Daily automated backups, 30-day retention
- **Implementation**: DynamoDB point-in-time recovery

---

### 4.4 Usability Requirements

#### NFR-USAB-001: User Interface
- **Priority**: High
- **Requirement**: Intuitive UI following Material Design principles
- **Measurement**: User testing with 90% task completion

#### NFR-USAB-002: Accessibility
- **Priority**: Medium
- **Requirement**: WCAG 2.1 Level AA compliance
- **Measurement**: Automated accessibility testing

#### NFR-USAB-003: Mobile Responsiveness
- **Priority**: High
- **Requirement**: Fully functional on mobile devices (320px+)
- **Measurement**: Responsive design testing

#### NFR-USAB-004: Browser Support
- **Priority**: High
- **Requirement**: Support Chrome, Firefox, Safari, Edge (latest 2 versions)
- **Measurement**: Cross-browser testing

---

### 4.5 Maintainability Requirements

#### NFR-MAINT-001: Code Quality
- **Priority**: Medium
- **Requirement**: Code coverage ≥ 80%
- **Measurement**: Jest/Pytest coverage reports

#### NFR-MAINT-002: Documentation
- **Priority**: Medium
- **Requirement**: Comprehensive API documentation
- **Implementation**: OpenAPI/Swagger specification

#### NFR-MAINT-003: Logging
- **Priority**: High
- **Requirement**: Structured logging for all operations
- **Implementation**: CloudWatch Logs with log levels

#### NFR-MAINT-004: Monitoring
- **Priority**: High
- **Requirement**: Real-time monitoring and alerting
- **Implementation**: CloudWatch dashboards and alarms

---

## 5. User Requirements

### 5.1 Administrator Requirements
- Manage user accounts and permissions
- Configure system settings
- View audit logs
- Generate compliance reports
- Manage alert thresholds

### 5.2 Investigator Requirements
- Review and investigate complaints
- Update complaint status
- Access audio/document evidence
- View beneficiary risk profiles
- Generate investigation reports

### 5.3 Analyst Requirements
- View analytics dashboards
- Generate custom reports
- Export data (CSV, PDF)
- View trends and patterns
- Access historical data

### 5.4 Public User Requirements
- Submit complaints (authenticated or anonymous)
- Upload audio/document evidence
- Track complaint status
- Receive notifications

---

## 6. System Requirements

### 6.1 Hardware Requirements

#### Frontend
- Modern web browser
- Minimum 2GB RAM
- Internet connection (1 Mbps+)

#### Backend (AWS Infrastructure)
- Lambda: 512MB-3GB memory per function
- DynamoDB: On-demand capacity mode
- S3: Standard storage class
- CloudFront: Global CDN

### 6.2 Software Requirements

#### Frontend
- Node.js 16+
- React 18+
- Tailwind CSS 3+
- Axios 1.6+
- Recharts 2.10+

#### Backend
- Python 3.9+
- FastAPI 0.100+
- Boto3 (AWS SDK)
- Pydantic for validation
- Mangum for Lambda integration

#### Database
- DynamoDB (NoSQL)
- Tables: beneficiaries, complaints, alerts, risk_scores

#### Storage
- S3 buckets for audio/documents
- CloudFront for CDN

---

## 7. Data Requirements

### 7.1 Data Models

#### Beneficiary
```
beneficiary_id: String (PK)
name: String
date_of_birth: String
gender: String
address: String
phone: String
bank_account_hash: String
district: String
state: String
scheme: String
amount: Number
risk_score: Number
risk_category: String
is_duplicate: Boolean
is_flagged: Boolean
created_at: String
```

#### Complaint
```
complaint_id: String (PK)
complaint_type: String
beneficiary_id: String
description: String
location: Object
audio_url: String
report_url: String
transcription_job: String
urgency_score: Number
sentiment_score: Number
status: String
submitter_name: String
submitter_phone: String
is_anonymous: Boolean
created_at: String
```

#### Alert
```
alert_id: String (PK)
alert_type: String
severity: String
beneficiary_id: String
risk_score: Number
title: String
description: String
status: String
created_at: String
```

#### Risk Score
```
beneficiary_id: String (PK)
timestamp: String (SK)
risk_score: Number
risk_category: String
duplicate_score: Number
anomaly_score: Number
network_centrality: Number
complaint_severity: Number
explanation: String
factors: Object
```

### 7.2 Data Retention
- Beneficiary data: Indefinite (until deletion request)
- Complaints: 7 years
- Alerts: 2 years
- Risk scores: 1 year
- Audio files: 5 years
- Logs: 90 days

### 7.3 Data Privacy
- PII encryption at rest and in transit
- Bank account hashing (SHA-256)
- Anonymous complaint support
- GDPR compliance (right to deletion)
- Access logging and audit trails

---

## 8. Integration Requirements

### 8.1 AWS Services Integration

#### INT-AWS-001: Lambda
- Serverless compute for API
- Auto-scaling based on load
- VPC integration for security

#### INT-AWS-002: DynamoDB
- NoSQL database for all data
- Global secondary indexes for queries
- Point-in-time recovery enabled

#### INT-AWS-003: S3
- Object storage for files
- Versioning enabled
- Lifecycle policies for cost optimization

#### INT-AWS-004: Transcribe
- Audio-to-text transcription
- Support for multiple languages
- Custom vocabulary for domain terms

#### INT-AWS-005: Cognito
- User authentication
- JWT token management
- User pool management

#### INT-AWS-006: CloudWatch
- Logging and monitoring
- Custom metrics and alarms
- Dashboard for operations

### 8.2 External Integrations

#### INT-EXT-001: Email Service
- Send notifications via SES
- Complaint status updates
- Alert notifications

#### INT-EXT-002: SMS Service
- Send SMS via SNS
- Critical alert notifications
- OTP for authentication

---

## 9. Security Requirements

### 9.1 Authentication & Authorization

#### SEC-AUTH-001: JWT Authentication
- Token-based authentication
- 24-hour token expiry
- Refresh token mechanism
- Secure token storage

#### SEC-AUTH-002: Role-Based Access Control
- User roles: admin, investigator, analyst, public
- Permission-based access
- Least privilege principle

### 9.2 Data Security

#### SEC-DATA-001: Encryption at Rest
- DynamoDB encryption enabled
- S3 bucket encryption (AES-256)
- KMS key management

#### SEC-DATA-002: Encryption in Transit
- HTTPS/TLS 1.2+ only
- Certificate management via ACM
- HSTS headers enabled

#### SEC-DATA-003: Data Masking
- Bank account hashing
- PII redaction in logs
- Sensitive field encryption

### 9.3 Application Security

#### SEC-APP-001: Input Validation
- Server-side validation for all inputs
- SQL injection prevention
- XSS prevention
- CSRF protection

#### SEC-APP-002: API Security
- Rate limiting (100 req/min per IP)
- API key authentication
- CORS configuration
- Request size limits

#### SEC-APP-003: File Upload Security
- File type validation
- File size limits
- Virus scanning
- Secure file storage

### 9.4 Network Security

#### SEC-NET-001: VPC Configuration
- Private subnets for Lambda
- Security groups for access control
- Network ACLs

#### SEC-NET-002: WAF Protection
- SQL injection rules
- XSS protection rules
- Rate limiting rules
- Geo-blocking if needed

---

## 10. Compliance Requirements

### 10.1 Data Protection

#### COMP-DATA-001: GDPR Compliance
- Right to access
- Right to deletion
- Right to rectification
- Data portability
- Consent management

#### COMP-DATA-002: Data Localization
- Data stored in India region (ap-south-1)
- Compliance with Indian data laws
- Cross-border data transfer restrictions

### 10.2 Audit & Reporting

#### COMP-AUDIT-001: Audit Logging
- Log all data access
- Log all modifications
- Log authentication events
- Tamper-proof logs

#### COMP-AUDIT-002: Compliance Reports
- Monthly security reports
- Quarterly compliance reports
- Annual audit reports
- Incident reports

### 10.3 Government Regulations

#### COMP-GOV-001: RTI Compliance
- Right to Information Act compliance
- Public disclosure requirements
- Response within 30 days

#### COMP-GOV-002: IT Act Compliance
- Information Technology Act 2000
- Reasonable security practices
- Data breach notification

---

## Appendix

### A. Glossary
- **Beneficiary**: Individual receiving welfare benefits
- **Fraud Score**: Calculated risk score (0.0-1.0)
- **Leakage**: Unauthorized diversion of funds
- **Ghost Beneficiary**: Fake/non-existent beneficiary
- **Duplicate**: Same person registered multiple times

### B. Assumptions
- Users have internet connectivity
- Users have modern web browsers
- AWS services are available
- Government data is accessible

### C. Constraints
- Budget limitations for AWS services
- Compliance with government regulations
- Data privacy requirements
- Performance requirements

### D. Dependencies
- AWS infrastructure availability
- Third-party service availability
- Government data sources
- Internet connectivity

---

**Document Version**: 1.0  
**Last Updated**: March 9, 2026  
**Status**: Approved  
**Next Review**: June 9, 2026
