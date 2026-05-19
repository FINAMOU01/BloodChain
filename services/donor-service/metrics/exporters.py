from prometheus_client import Counter, Histogram, Gauge

DONOR_REGISTRATIONS = Counter('bloodchain_donor_registrations_total', 'Total number of donor registrations')
BLOOD_BAGS_COLLECTED = Counter('bloodchain_blood_bags_collected_total', 'Total number of blood bags collected')
BLOOD_REQUESTS_CREATED = Counter('bloodchain_blood_requests_total', 'Total number of hospital blood requests')
EMERGENCY_ALERTS_SENT = Counter('bloodchain_emergency_alerts_total', 'Total number of emergency alerts sent')
REWARDS_MINTED = Counter('bloodchain_rewards_minted_total', 'Total tokens minted for donors')

API_RESPONSE_TIME = Histogram(
    'bloodchain_api_response_seconds',
    'API response time in seconds',
    buckets=(0.1, 0.25, 0.5, 1.0, 2.5, 5.0)
)
