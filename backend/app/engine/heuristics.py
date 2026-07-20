import math
import urllib.parse
import re

def get_entropy(text: str) -> float:
    if not text:
        return 0.0
    length = len(text)
    frequencies = {}
    for char in text:
        frequencies[char] = frequencies.get(char, 0) + 1
    entropy = 0.0
    for freq in frequencies.values():
        p = freq / length
        entropy -= p * math.log2(p)
    return entropy

def analyze_url(url_str: str):
    if not url_str.startswith("http"):
        url_str = "https://" + url_str
    
    try:
        parsed = urllib.parse.urlparse(url_str)
        if not parsed.hostname:
            return {"error": "Invalid URL format."}
    except Exception:
        return {"error": "Invalid URL format."}

    results = []
    total_score = 0

    # 1. IP Detector
    if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", parsed.hostname):
        results.append({
            "id": "ip-detector",
            "name": "IP Address Host",
            "severity": "critical",
            "score": 80,
            "explanation": "The URL uses an IP address instead of a domain name, a common technique to hide identity.",
            "recommendation": "Do not proceed. Legitimate services use domain names.",
            "evidence": parsed.hostname
        })
        total_score += 80

    # 2. Length Detector
    if len(url_str) > 100:
        score = min(40, (len(url_str) - 100) / 2)
        results.append({
            "id": "length-detector",
            "name": "Suspicious Length",
            "severity": "warning",
            "score": int(score),
            "explanation": f"URL is unusually long ({len(url_str)} characters), which can be used to obfuscate malicious payloads.",
            "recommendation": "Inspect the URL parameters carefully.",
            "evidence": f"Length: {len(url_str)}"
        })
        total_score += int(score)

    # 3. Keyword Detector
    keywords = ['login', 'secure', 'account', 'verify', 'update', 'banking', 'auth', 'confirm']
    found_keywords = [k for k in keywords if k in url_str.lower()]
    if found_keywords:
        score = 30 * len(found_keywords)
        results.append({
            "id": "keyword-detector",
            "name": "Deceptive Keywords",
            "severity": "high" if len(found_keywords) > 1 else "warning",
            "score": score,
            "explanation": "URL contains sensitive keywords often used in social engineering.",
            "recommendation": "Verify if the sender is legitimate before proceeding.",
            "evidence": ", ".join(found_keywords)
        })
        total_score += score

    # 4. Subdomain Detector
    parts = parsed.hostname.split('.')
    if len(parts) > 3 and parts[0] != 'www':
        score = 25 + ((len(parts) - 3) * 10)
        results.append({
            "id": "subdomain-detector",
            "name": "Excessive Subdomains",
            "severity": "warning",
            "score": score,
            "explanation": f"URL has an unusual number of subdomains ({len(parts)}), a technique used to spoof legitimate domains.",
            "recommendation": "Check the root domain carefully.",
            "evidence": parsed.hostname
        })
        total_score += score

    # 5. TLD Detector
    tld = parts[-1].lower() if parts else ""
    suspicious_tlds = ['xyz', 'top', 'live', 'gq', 'ml', 'cf', 'tk', 'ga', 'buzz', 'cn', 'ru']
    if tld in suspicious_tlds:
        results.append({
            "id": "tld-detector",
            "name": "Suspicious TLD",
            "severity": "high",
            "score": 45,
            "explanation": f"The Top Level Domain (.{tld}) has a historically high rate of abuse.",
            "recommendation": "Exercise extreme caution, even if the site appears legitimate.",
            "evidence": f".{tld}"
        })
        total_score += 45

    # 6. Entropy Detector
    domain_entropy = get_entropy(parsed.hostname)
    path_entropy = get_entropy(parsed.path)
    query_entropy = get_entropy(parsed.query)
    max_entropy = max(domain_entropy, path_entropy, query_entropy)

    if max_entropy > 4.5:
        results.append({
            "id": "entropy-detector",
            "name": "High Character Entropy",
            "severity": "high",
            "score": 35,
            "explanation": "High structural entropy detected, indicating randomly generated domains (DGA) or obfuscated paths.",
            "recommendation": "Do not click or interact with random alphanumeric links.",
            "evidence": f"Entropy: {max_entropy:.2f}"
        })
        total_score += 35

    final_score = min(100, int(total_score))
    
    if final_score >= 75:
        risk_level = "Critical"
    elif final_score >= 40:
        risk_level = "Suspicious"
    elif final_score > 0:
        risk_level = "Low Risk"
    else:
        risk_level = "Safe"

    return {
        "url": url_str,
        "protocol": parsed.scheme + ":",
        "hostname": parsed.hostname,
        "pathname": parsed.path or "/",
        "searchParams": parsed.query or "None",
        "score": final_score,
        "riskLevel": risk_level,
        "confidence": "High",
        "entropies": {
            "domain": f"{domain_entropy:.2f}",
            "path": f"{path_entropy:.2f}",
            "query": f"{query_entropy:.2f}",
            "max": f"{max_entropy:.2f}"
        },
        "findings": results
    }
