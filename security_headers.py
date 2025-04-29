from typing import Dict

def get_security_headers() -> Dict[str, str]:
    """
    Return a dictionary of security headers to be applied to all responses.
    These headers help protect against various web vulnerabilities.
    """
    return {
        # Prevent browsers from interpreting files as a different MIME type
        'X-Content-Type-Options': 'nosniff',
        
        # Protect against clickjacking
        'X-Frame-Options': 'SAMEORIGIN',
        
        # Enable browser's XSS filter
        'X-XSS-Protection': '1; mode=block',
        
        # Control how much information is sent in the Referer header
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        
        # Specify valid sources for content
        'Content-Security-Policy': "default-src 'self' https:; script-src 'self' 'unsafe-inline' 'unsafe-eval' https:; style-src 'self' 'unsafe-inline' https:; img-src 'self' data: https:; font-src 'self' https:; connect-src 'self' https:;",
        
        # Enable HSTS (force HTTPS)
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        
        # Prevent MIME type sniffing
        'X-Content-Type-Options': 'nosniff',
        
        # Control browser features
        'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
    }

def apply_security_headers(response):
    """
    Apply security headers to a response object.
    """
    headers = get_security_headers()
    for header, value in headers.items():
        response.headers[header] = value
    return response 