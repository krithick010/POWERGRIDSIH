-- Seed some sample tickets for testing
INSERT INTO tickets (source, employee, subject, description, priority, category, assigned_team, status) VALUES
(
    'chatbot',
    'Rajesh Kumar (PG12345)',
    'Cannot access VPN from home',
    'I am trying to connect to VPN from my home network but getting "Connection Failed" error. I have checked my internet connection and it is working fine. Please help.',
    'high',
    'network',
    'Network Team',
    'in_progress'
),
(
    'email',
    'Priya Sharma (PG12346)',
    'Password reset required',
    'My password has expired and I need to reset it. I tried the self-service portal but not receiving the reset email.',
    'medium',
    'access',
    'IT Support',
    'open'
),
(
    'glpi',
    'Amit Patel (PG12347)',
    'Laptop screen flickering',
    'My laptop screen has started flickering intermittently. It happens more frequently when running multiple applications. The laptop is 2 years old.',
    'medium',
    'hardware',
    'Hardware Support',
    'open'
),
(
    'chatbot',
    'Sneha Reddy (PG12348)',
    'Need Microsoft Project license',
    'I require Microsoft Project Professional license for the new infrastructure project. Budget code: INFRA-2025-001. Manager approval attached.',
    'low',
    'software',
    'Software Licensing',
    'resolved'
),
(
    'solman',
    'Vikram Singh (PG12349)',
    'Cannot access S drive folder',
    'I need access to S:\\Engineering\\Transmission\\Reports folder for my current assignment. My manager has approved this access.',
    'medium',
    'access',
    'IT Support',
    'resolved'
);
