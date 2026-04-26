import httpx
from datetime import datetime

async def run_validation_checks(api_endpoint: str, auth_method: str, ad_platform: str) -> list:
    checks = []
    start = datetime.utcnow()
    # Check 1 — Endpoint Reachability
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_endpoint, timeout=5.0)
        
        checks.append({
            "check_type": "Endpoint Reachability",
            "passed": response.status_code < 500,  # what condition makes this pass?
            "severity": "critical",
            "message": f"Endpoint returned status {response.status_code}",
            "fix": None if response.status_code < 500 else "Verify endpoint URL is correct"  # None if passed, string if failed
        })
    except Exception as e:
        checks.append({
            "check_type": "Endpoint Reachability",
            "passed": False,
            "severity": "critical",
            "message": f"Could not reach endpoint: {str(e)}",
            "fix": "Check if endpoint URL is correct and accessible"
        })
        
    #Check 2 — Response Latency
    latency = (datetime.utcnow() - start).total_seconds() * 1000
    checks.append({
        "check_type": "Response Time",
        "passed": latency < 2000,  # passes if latency under 2000ms
        "severity": "warning",
        "message": f"Response time: {latency:.0f}ms",
        "fix": None if latency < 2000 else "Consider implementing caching to reduce latency" 
    })
    
    #Check 3 — HTTPS Security
    checks.append({
        "check_type": "HTTPS Security",
        "passed": api_endpoint.startswith("https://"),
        "severity": "critical",
        "message": "Endpoint is using HTTPS" if api_endpoint.startswith("https://") else "Endpoint is not using HTTPS",
        "fix": None if api_endpoint.startswith("https://") else "Use HTTPS instead of HTTP"
    })
    
    
    
    #Check 4 — Auth Method Validity
    valid_auth = {
    "GoogleAdManager": ["OAuth", "JWT"],
    "AdSense":         ["OAuth", "APIKey"],
    "AdMob":           ["OAuth", "APIKey"]
    }
    is_valid_auth = auth_method in valid_auth.get(ad_platform, [])
    checks.append({
        "check_type": "Authentication Method",
        "passed": is_valid_auth,
        "severity": "critical",
        "message": f"{auth_method} is valid for {ad_platform}" if is_valid_auth else f"{auth_method} is invalid for {ad_platform}",
        "fix": None if is_valid_auth else f"Use one of {valid_auth.get(ad_platform)} for {ad_platform}"
    })
    
    '''print(f"auth_method received: {auth_method}")
    print(f"ad_platform received: {ad_platform}")
    print(f"valid_auth lookup: {valid_auth.get(ad_platform, [])}")
    print(f"is_valid_auth: {is_valid_auth}")'''

    return checks

    