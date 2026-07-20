import { detectors } from "./detectors";

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

export const analyzeURL = (urlStr) => {
  let urlObj;
  try {
    urlObj = new URL(urlStr.startsWith("http") ? urlStr : `https://${urlStr}`);
  } catch (e) {
    return { error: "Invalid URL format." };
  }

  const results = [];
  let totalScore = 0;

  for (const detector of detectors) {
    const res = detector.analyze(urlObj);
    if (res.triggered) {
      results.push({
        id: detector.id,
        name: detector.name,
        ...res,
      });
      totalScore += res.score;
    }
  }

  const finalScore = Math.min(100, Math.round(totalScore));

  let riskLevel = "Safe";
  let confidence = "High";

  if (finalScore >= 75) {
    riskLevel = "Critical";
  } else if (finalScore >= 40) {
    riskLevel = "Suspicious";
  } else if (finalScore > 0) {
    riskLevel = "Low Risk";
  }

  // Calculate entropies for the summary
  const domainEntropy = getEntropy(urlObj.hostname);
  const pathEntropy = getEntropy(urlObj.pathname);
  const queryEntropy = getEntropy(urlObj.search);

  return {
    url: urlObj.href,
    protocol: urlObj.protocol,
    hostname: urlObj.hostname,
    pathname: urlObj.pathname,
    searchParams: urlObj.search,
    score: finalScore,
    riskLevel,
    confidence,
    entropies: {
      domain: domainEntropy.toFixed(2),
      path: pathEntropy.toFixed(2),
      query: queryEntropy.toFixed(2),
      max: Math.max(domainEntropy, pathEntropy, queryEntropy).toFixed(2),
    },
    findings: results,
  };
};
