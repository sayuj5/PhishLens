export const detectors = [
  {
    id: "ip-detector",
    name: "IP Address Host",
    description: "Checks if the domain is an IP address.",
    analyze: (urlObj) => {
      const isIP = /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/.test(urlObj.hostname);
      if (isIP) {
        return {
          triggered: true,
          score: 80,
          severity: "critical",
          explanation:
            "The URL uses an IP address instead of a domain name, a common technique to hide identity.",
          recommendation:
            "Do not proceed. Legitimate services use domain names.",
          evidence: urlObj.hostname,
        };
      }
      return { triggered: false };
    },
  },
  {
    id: "length-detector",
    name: "Suspicious Length",
    description: "Flags unusually long URLs.",
    analyze: (urlObj) => {
      const length = urlObj.href.length;
      if (length > 100) {
        return {
          triggered: true,
          score: Math.min(40, (length - 100) / 2),
          severity: "warning",
          explanation: `URL is unusually long (${length} characters), which can be used to obfuscate malicious payloads.`,
          recommendation: "Inspect the URL parameters carefully.",
          evidence: `Length: ${length}`,
        };
      }
      return { triggered: false };
    },
  },
  {
    id: "keyword-detector",
    name: "Deceptive Keywords",
    description: "Looks for deceptive keywords in the URL.",
    analyze: (urlObj) => {
      const keywords = [
        "login",
        "secure",
        "account",
        "verify",
        "update",
        "banking",
        "auth",
        "confirm",
      ];
      const found = keywords.filter((k) =>
        urlObj.href.toLowerCase().includes(k),
      );
      if (found.length > 0) {
        return {
          triggered: true,
          score: 30 * found.length,
          severity: found.length > 1 ? "high" : "warning",
          explanation: `URL contains sensitive keywords often used in social engineering.`,
          recommendation:
            "Verify if the sender is legitimate before proceeding.",
          evidence: found.join(", "),
        };
      }
      return { triggered: false };
    },
  },
  {
    id: "subdomain-detector",
    name: "Excessive Subdomains",
    description: "Evaluates the depth of subdomains.",
    analyze: (urlObj) => {
      const parts = urlObj.hostname.split(".");
      if (parts.length > 3 && parts[0] !== "www") {
        return {
          triggered: true,
          score: 25 + (parts.length - 3) * 10,
          severity: "warning",
          explanation: `URL has an unusual number of subdomains (${parts.length}), a technique used to spoof legitimate domains.`,
          recommendation: "Check the root domain carefully.",
          evidence: urlObj.hostname,
        };
      }
      return { triggered: false };
    },
  },
  {
    id: "tld-detector",
    name: "Suspicious TLD",
    description: "Flags unusual or frequently abused Top Level Domains.",
    analyze: (urlObj) => {
      const parts = urlObj.hostname.split(".");
      const tld = parts[parts.length - 1].toLowerCase();
      const suspiciousTLDs = [
        "xyz",
        "top",
        "live",
        "gq",
        "ml",
        "cf",
        "tk",
        "ga",
        "buzz",
        "cn",
        "ru",
      ];
      if (suspiciousTLDs.includes(tld)) {
        return {
          triggered: true,
          score: 45,
          severity: "high",
          explanation: `The Top Level Domain (.${tld}) has a historically high rate of abuse.`,
          recommendation:
            "Exercise extreme caution, even if the site appears legitimate.",
          evidence: `.${tld}`,
        };
      }
      return { triggered: false };
    },
  },
  {
    id: "entropy-detector",
    name: "High Character Entropy",
    description:
      "Calculates structural entropy to detect randomly generated domains or paths.",
    analyze: (urlObj) => {
      const getEntropy = (str) => {
        if (!str) return 0;
        const len = str.length;
        const frequencies = Array.from(str).reduce((freq, c) => {
          freq[c] = (freq[c] || 0) + 1;
          return freq;
        }, {});
        return Object.values(frequencies).reduce((sum, f) => {
          const p = f / len;
          return sum - p * Math.log2(p);
        }, 0);
      };

      const domainEntropy = getEntropy(urlObj.hostname);
      const pathEntropy = getEntropy(urlObj.pathname);
      const queryEntropy = getEntropy(urlObj.search);
      const maxEntropy = Math.max(domainEntropy, pathEntropy, queryEntropy);

      if (maxEntropy > 4.5) {
        return {
          triggered: true,
          score: 35,
          severity: "high",
          explanation: `High structural entropy detected, indicating randomly generated domains (DGA) or obfuscated paths.`,
          recommendation:
            "Do not click or interact with random alphanumeric links.",
          evidence: `Entropy: ${maxEntropy.toFixed(2)}`,
        };
      }
      return { triggered: false };
    },
  },
];
