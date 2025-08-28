# 🚨 What exactly is the Problem Statement?
Flixkart, a leading e-commerce platform, has recently undergone a security audit. While our primary data repositories are fortified, a significant vulnerability has been identified: a potential data leakage through unmonitored assets. A recent fraud incident, where a customer's personal details (name and address) were used to create a fraudulent order, traced back to logs from an external API integration. These logs were passing through a network ingress layer and were not being adequately sanitized. This PII leak led to a series of telephonic frauds where customers were scammed into giving away OTPs, resulting in unauthorized orders and refund scams. Furthermore, unmonitored endpoints were found to be storing PII in plain text, and some PII was even being rendered in internal web applications, creating further security risks. 

# 🧠 My understanding
Firstly, Flixkart has a PII leakage vulnerability across multiple unmonitored touchpoints in their infrastructure, which has already led to real financial fraud and customer harm.

# ⚠️ Pain points I observed
1. **Log Contamination** - Logs from API Integrations from external third-party resources are often unsanitized. These external logs pass through the company's internal network without filtering. No real time monitoring or encryption of sensitive data in logs. This falls under **A09 – Security Logging and Monitoring Failures** in the **OWASP Top 10**.

2. **Application Exposure** - Internal web applications can reder PII directly which can lead to unauthorized access.

3. **Impact on Customers** - Leaked phone numbers can be used by scammers in telephonic fraud schemes like Digital arrests, etc. Scammers can obtain customer details to request OTPs. This can also lead to unauthorized orders and refund scams.

#  💻 How I am implementing the code to solve the problems
Link to code - https://github.com/juikalan21/Real-time-PII-Defense-/blob/main/detector_full_jui_kalan.py 

The tool hides/redacts/masks the Personally Identifiable Information (PII) data like:
- Names (first name, last name, full name)
- Phone numbers
- Email addresses  
- Aadhar Card numbers
- Passport numbers
- UPI IDs 
- IP addresses
- Physical addresses
- PIN codes

<img width="851" height="984" alt="PII " src="https://github.com/user-attachments/assets/17ecf5a8-05b4-44a7-b74a-48e557831e92" />

# 📦 Installation
```sh
pip install pandas
```
On Linux
```sh
python3 detector_full_jui_kalan.py iscp_pii_dataset.csv
```
On Windows
```sh
python detector_full_jui_kalan.py iscp_pii_dataset.csv
```
# 🌟 Why this project matters!
Every day companies are bleeding money from data breaches. Real-time PII Defense works because traditional security solutions are like installing locks on your front door while leaving all your windows wide open. Companies process millions of customer records daily through APIs, logs, databases, and external integrations, but even just a single unredacted phone number in a log file can lead to customer fraud, regulatory fines, and destroyed trust.

**My solution doesn't just detect PII, it actively protects it in real-time across your entire data pipeline.** Think of it as having an intelligent security guard who never sleeps, never misses a detail, and works at the speed of your business.

**There are multiple applications for this tool:**
- **E-commerce platforms** certified with ISO 27001 for its Business Continuity Management System (BCMS).
- **Financial service**s maintaining PCI DSS.
-** Healthcare systems** adhered to HIPAA.
- And literally any company that can't afford a data breach lawsuit or compliance failure :)


# 🚀 My Deployment strategy
## 1. Foundation Setup
My main focus is to use open source deployment resouces as much as I could. I will install the core PII detection engine at API Gateway level. Think of the API Gateway as the main entrance to a building. Every person (data request) has to pass through this entrance before going anywhere else in the building. This is the perfect place to put our main security guard. Main factors are that one checkpoint covers everything, quick inspection, cost effective and easy to manage. 

Tools I think will work:
- **Docker** for containerization.
- **Kubernetes** for orchestration.
- **Prometheus** for traffic management, monitoring and user-friendly dashboards.

## 2. Application and Network Layer Monitoring
Embedding PII protection directly into your applications and deploying network wide PII Detection. This creates our second layer of defense. Even if something bypasses the API gateway, we catch it at the application level. 

Tools I think will work:
- **Redis** for caching frequently detected patterns
- **PostgreSQL** for database audit logging (using pgAudit, a open source extension)
- **ELK Stack** (Elasticsearch, Logstash, Kibana) for comprehensive logging - This is our perimeter defense which makes sure no PII leaves the company's network without authorization.

## 3. Security Integration (DevSecOps)
Having some prior knowledge and hands on experience in DevSecOps, I will surely implement it in my PII Defense system because security needs to be integrated into every phase of the software development lifecycle. DevSecOps embeds security checks early and often which means the PII detection and redaction happens during development via automation, not after production deployment.

DevSecOps tools I have used and which will work here also:
- **SonarQube** will automatically scan our PII detection code for vulnerabilities.
- **OWASP** can be used during Docker image building in all phases, and dependency scanning for known vulnerabilities in our libraries.
- **Trivy** scans our Docker images for OS vulnerabilities

### **Why DevSecOps is Critical Here:**
- **Speed matters**: Our business can't wait weeks for security reviews.
- **Scale demands automation**: We can't manually review millions of API calls.
- **Responsibility is shared**: Everyone owns PII protection, not just the security team.

# 🏗️ Architecture Diagram
<img width="2214" height="3032" alt="Deployment Architecture" src="https://github.com/user-attachments/assets/c855bb80-7496-46c2-a62a-182c32c70e57" />

# ⚡ How well it addresses the constraints of latency, cost, and scale?
My PII Defense project excels in addressing critical constraints like: 
- **Latency** - API Gateway results in <10ms overhead through in-process communication, reducing the data packets forwarding
- **Cost** - Leverages existing infrastructure with open-source tools (Docker, Kubernetes, Redis) avoiding separate deployments.
- **Scale** - Inherits auto-scaling from API Gateway, handling traffic growth seamlessly through Kubernetes horizontal scaling without manual intervention.
  
# 🎯Conclusion:
API Gateway placement delivers enterprise-grade PII protection that scales with business growth, operates with minimal performance impact, requires minimal investment, and integrates seamlessly with existing operations. It's not just good security - it's smart business.

All diagrams made using - https://excalidraw.com/ 




 


