# WHAT EXACTLY IS THE PROBLEM STATEMENT?
Flixkart, a leading e-commerce platform, has recently undergone a security audit. While our primary data repositories are fortified, a significant vulnerability has been identified: a potential data leakage through unmonitored assets. A recent fraud incident, where a customer's personal details (name and address) were used to create a fraudulent order, traced back to logs from an external API integration. These logs were passing through a network ingress layer and were not being adequately sanitized. This PII leak led to a series of telephonic frauds where customers were scammed into giving away OTPs, resulting in unauthorized orders and refund scams. Furthermore, unmonitored endpoints were found to be storing PII in plain text, and some PII was even being rendered in internal web applications, creating further security risks. 

# MY UNDERSTANDING
Firstly, Flixkart has a PII leakage vulnerability across multiple unmonitored touchpoints in their infrastructure, which has already led to real financial fraud and customer harm.

# PAIN POINTS I OBSERVED
1. **Log Contamination** - Logs from API Integrations from external third-party resources are often unsanitized. These external logs pass through the company's internal network without filtering. No real time monitoring or encryption of sensitive data in logs. This falls under **A09 – Security Logging and Monitoring Failures** in the **OWASP Top 10**.

2. **Application Exposure** - Internal web applications can reder PII directly which can lead to unauthorized access.

3. **Impact on Customers** - Leaked phone numbers can be used by scammers in telephonic fraud schemes like Digital arrests, etc. Scammers can obtain customer details to request OTPs. This can also lead to unauthorized orders and refund scams.

# HOW I AM IMPLEMENTING THE CODE TO SOLVE THESE PROBLEMS
<img width="851" height="984" alt="PII " src="https://github.com/user-attachments/assets/17ecf5a8-05b4-44a7-b74a-48e557831e92" />
 
