-- Seed knowledge base with common IT support articles
INSERT INTO knowledge_base (title, content, category, keywords) VALUES
(
    'How to Reset Your Password',
    'To reset your POWERGRID password:
    
1. Go to the password reset portal at https://password.powergrid.in
2. Enter your employee ID and registered email address
3. Click "Send Reset Link"
4. Check your email for the password reset link (valid for 24 hours)
5. Click the link and enter your new password
6. Your new password must be at least 8 characters with uppercase, lowercase, numbers, and special characters
7. Confirm your new password and click "Reset Password"

If you do not receive the email within 15 minutes, check your spam folder or contact IT support at ext. 2222.

Note: Your password will expire every 90 days for security purposes.',
    'access',
    ARRAY['password', 'reset', 'login', 'access', 'forgot password', 'account locked']
),
(
    'VPN Setup and Connection Guide',
    'Setting up VPN access for remote work:

**Initial Setup:**
1. Download Cisco AnyConnect VPN client from https://vpn.powergrid.in/downloads
2. Install the client on your device (Windows/Mac/Linux supported)
3. Launch Cisco AnyConnect
4. Enter VPN address: vpn.powergrid.in
5. Click Connect

**Login Credentials:**
- Username: Your employee ID (e.g., PG12345)
- Password: Your POWERGRID network password
- Two-Factor Authentication: Enter the 6-digit code from your authenticator app

**Troubleshooting:**
- If connection fails, ensure you are using the latest VPN client version
- Check your internet connection
- Verify your credentials are correct
- Contact IT support if you need VPN access enabled for your account

**Security Note:** Always disconnect VPN when not in use. Do not share your VPN credentials.',
    'network',
    ARRAY['vpn', 'remote access', 'cisco anyconnect', 'work from home', 'connection', 'network']
),
(
    'Email Configuration on Mobile Devices',
    'Configure your POWERGRID email on mobile devices:

**For Android:**
1. Open Settings > Accounts > Add Account
2. Select "Exchange" or "Corporate"
3. Enter your email: firstname.lastname@powergrid.in
4. Password: Your network password
5. Server: mail.powergrid.in
6. Domain: POWERGRID
7. Username: Your employee ID
8. Tap Next and accept security policies

**For iPhone/iPad:**
1. Go to Settings > Mail > Accounts > Add Account
2. Select "Microsoft Exchange"
3. Email: firstname.lastname@powergrid.in
4. Description: POWERGRID Email
5. Tap Next
6. Server: mail.powergrid.in
7. Domain: POWERGRID
8. Username: Your employee ID
9. Password: Your network password
10. Tap Next and enable Mail, Contacts, Calendars as needed

**Common Issues:**
- If authentication fails, verify your password is correct
- Ensure your device meets minimum security requirements
- Contact IT if your account is not enabled for mobile access',
    'software',
    ARRAY['email', 'mobile', 'outlook', 'exchange', 'android', 'iphone', 'configuration']
),
(
    'Requesting New Hardware or Equipment',
    'Process for requesting new hardware or equipment:

**Eligible Items:**
- Desktop computers and monitors
- Laptops for authorized personnel
- Printers and scanners
- Keyboards, mice, and accessories
- Network equipment (switches, routers)

**Request Process:**
1. Obtain approval from your Department Head
2. Fill out Hardware Request Form (available on intranet)
3. Submit form to IT Asset Management at itassets@powergrid.in
4. Include justification and budget code
5. Wait for approval (typically 3-5 business days)
6. Once approved, procurement will process the order
7. Delivery timeline: 2-4 weeks depending on availability

**Urgent Requests:**
For urgent hardware needs, mark the request as "URGENT" and contact IT support directly at ext. 2222.

**Replacement of Faulty Equipment:**
If your current equipment is faulty, create a ticket describing the issue. IT will assess and arrange replacement if necessary.',
    'hardware',
    ARRAY['hardware', 'equipment', 'laptop', 'desktop', 'computer', 'printer', 'request', 'new']
),
(
    'Software Installation and License Requests',
    'How to request software installation or licenses:

**Pre-Approved Software:**
The following software can be installed by IT upon request:
- Microsoft Office Suite
- Adobe Acrobat Reader
- Web browsers (Chrome, Firefox, Edge)
- Zoom, Microsoft Teams
- Antivirus software

**Request Process:**
1. Create a ticket specifying the software name and version
2. Provide business justification
3. Obtain manager approval
4. IT will verify license availability
5. Installation will be scheduled within 2-3 business days

**Licensed Software:**
For software requiring purchase:
1. Submit request with cost estimate
2. Obtain budget approval from Finance
3. Provide purchase order number
4. IT will procure and install after license acquisition

**Security Note:**
- Never install unauthorized software
- All software must be approved by IT Security
- Using pirated software is strictly prohibited and may result in disciplinary action

**Open Source Software:**
Open source software requests must be reviewed by IT Security before installation.',
    'software',
    ARRAY['software', 'installation', 'license', 'application', 'program', 'microsoft', 'adobe']
),
(
    'Network Drive Access and Permissions',
    'Accessing network drives and managing permissions:

**Available Network Drives:**
- H: Drive - Personal home directory (100GB quota)
- S: Drive - Shared departmental folders
- P: Drive - Project-specific folders
- T: Drive - Temporary file storage (auto-deleted after 30 days)

**Accessing Network Drives:**
1. On Windows: Open File Explorer, drives should be mapped automatically
2. If not visible, go to "This PC" and click "Map Network Drive"
3. Enter path: \\\\fileserver.powergrid.in\\[drive-letter]
4. Check "Reconnect at sign-in"
5. Enter your network credentials if prompted

**Requesting Access:**
To request access to a shared folder:
1. Create a ticket specifying the folder path
2. Provide business justification
3. Obtain approval from the folder owner/manager
4. IT will grant access within 1 business day

**Permission Issues:**
If you cannot access a folder you should have access to:
- Verify you are connected to the network/VPN
- Check if your account is active
- Contact the folder owner to verify permissions
- Create a ticket if the issue persists

**Quota Management:**
Monitor your H: drive usage. If you exceed quota, you will not be able to save new files.',
    'network',
    ARRAY['network drive', 'shared folder', 'file access', 'permissions', 'h drive', 's drive', 'storage']
);
