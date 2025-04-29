from typing import Dict

def get_security_headers() -> Dict[str, str]:
    """
    Return a dictionary of security headers to be applied to all responses.
    These headers help protect against various web vulnerabilities and establish trust.
    """
    return {
        # Prevent browsers from interpreting files as a different MIME type
        'X-Content-Type-Options': 'nosniff',
        
        # Protect against clickjacking
        'X-Frame-Options': 'DENY',
        
        # Enable browser's XSS filter
        'X-XSS-Protection': '1; mode=block',
        
        # Control how much information is sent in the Referer header
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        
        # Specify valid sources for content
        'Content-Security-Policy': "\
            default-src 'self' https:; \
            script-src 'self' 'unsafe-inline' 'unsafe-eval' https: *.northwestern.edu; \
            style-src 'self' 'unsafe-inline' https: fonts.googleapis.com; \
            img-src 'self' data: https: *.northwestern.edu; \
            font-src 'self' https: fonts.gstatic.com; \
            connect-src 'self' https: api.nuanswers.org; \
            frame-ancestors 'none'; \
            form-action 'self'; \
            base-uri 'self'; \
            upgrade-insecure-requests; \
            block-all-mixed-content;",
        
        # Enable HSTS (force HTTPS)
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
        
        # Control browser features
        'Permissions-Policy': 'camera=(), microphone=(), geolocation=(), interest-cohort=()',
        
        # Add Northwestern University affiliation
        'X-Institution': 'Northwestern University',
        
        # Add contact information for security researchers
        'X-Security-Contact': 'security@nuanswers.org',
        
        # Add additional trust signals
        'X-Powered-By': 'Render.com',
        'X-DNS-Prefetch-Control': 'on',
        'Expect-CT': 'max-age=86400, enforce',
        
        # Cross-Origin headers
        'Cross-Origin-Opener-Policy': 'same-origin',
        'Cross-Origin-Resource-Policy': 'same-site',
        'Cross-Origin-Embedder-Policy': 'require-corp'
    }

def apply_security_headers(response):
    """
    Apply security headers to a response object.
    """
    headers = get_security_headers()
    for header, value in headers.items():
        response.headers[header] = value
    return response 