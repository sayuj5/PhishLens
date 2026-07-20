import { useState, useEffect, useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ArrowLeft,
  Shield,
  AlertTriangle,
  CheckCircle,
  Download,
  Copy,
  Info,
} from "lucide-react";
import { useReactToPrint } from "react-to-print";
import { AnimatedRiskMeter } from "../components/AnimatedRiskMeter";
import { analyzeURL } from "../engine/Analyzer";

const SkeletonLoader = () => (
  <div className="flex-1 py-8 flex flex-col gap-8 animate-pulse">
    <div className="h-8 bg-white/5 w-48 rounded"></div>
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div className="glass-panel p-10 h-125 bg-white/5 border-white/5"></div>
      <div className="lg:col-span-2 flex flex-col gap-6">
        <div className="glass-panel p-10 h-48 bg-white/5 border-white/5"></div>
        <div className="glass-panel p-10 h-64 bg-white/5 border-white/5"></div>
      </div>
    </div>
  </div>
);

export default function ReportPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const reportRef = useRef();

  useEffect(() => {
    const url = location.state?.urlToAnalyze;
    if (!url) {
      navigate("/");
      return;
    }

    // Simulate deep analysis delay for UX
    const timer = setTimeout(() => {
      setResult(analyzeURL(url));
      setIsLoading(false);
    }, 1500);

    return () => clearTimeout(timer);
  }, [location, navigate]);

  const handlePrint = useReactToPrint({
    contentRef: reportRef,
    documentTitle: "PhishLens_Report",
  });

  const handleCopyJSON = () => {
    if (result) {
      navigator.clipboard.writeText(JSON.stringify(result, null, 2));
      alert("Report JSON copied to clipboard");
    }
  };

  if (isLoading) {
    return <SkeletonLoader />;
  }

  if (result?.error) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-center">
        <AlertTriangle className="w-16 h-16 text-danger mb-6" />
        <h2 className="text-2xl font-display font-bold text-white mb-4">
          Analysis Failed
        </h2>
        <p className="text-textSecondary">{result.error}</p>
        <button
          onClick={() => navigate("/")}
          className="mt-8 bg-white/10 px-6 py-3 hover:bg-white/20 transition-colors rounded"
        >
          Go Back
        </button>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="flex-1 py-8 flex flex-col"
    >
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-8">
        <button
          onClick={() => navigate("/")}
          className="text-xs font-bold tracking-[0.2em] text-textSecondary hover:text-white uppercase flex items-center gap-3 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" /> NEW SCAN
        </button>
        <div className="flex flex-wrap gap-4 w-full md:w-auto">
          <button
            onClick={handleCopyJSON}
            className="flex-1 md:flex-none justify-center flex items-center gap-2 text-xs font-bold tracking-widest text-textPrimary bg-white/5 hover:bg-white/10 px-4 py-3 md:py-2 rounded transition-colors"
          >
            <Copy className="w-4 h-4" /> COPY JSON
          </button>
          <button
            onClick={handlePrint}
            className="flex-1 md:flex-none justify-center flex items-center gap-2 text-xs font-bold tracking-widest text-[#0d0c0c] bg-accent hover:bg-orange-500 px-4 py-3 md:py-2 rounded transition-colors"
          >
            <Download className="w-4 h-4" /> EXPORT PDF
          </button>
        </div>
      </div>

      <div ref={reportRef} className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Score & Entropy */}
        <div className="flex flex-col gap-8">
          <div className="glass-panel p-10 flex flex-col items-center justify-center min-h-112.5 relative hover:-translate-y-1 transition-transform duration-300">
            <div className="absolute top-0 left-0 w-full h-1 bg-linear-to-r from-transparent via-glow/20 to-transparent"></div>
            <h2 className="text-xs font-bold tracking-[0.2em] text-textSecondary uppercase mb-12">
              Overall Assessment
            </h2>
            <AnimatedRiskMeter score={result.score} />

            <div className="mt-12 text-center">
              <div
                className="text-3xl font-display font-bold tracking-widest uppercase"
                style={{
                  color:
                    result.score >= 75
                      ? "#ef4444"
                      : result.score >= 40
                        ? "#f59e0b"
                        : "#33d69f",
                }}
              >
                {result.riskLevel}
              </div>
              <div className="text-textSecondary/80 text-xs mt-4 tracking-wider break-all max-w-62.5">
                {result.url}
              </div>
            </div>
          </div>

          <div className="glass-panel p-8 hover:-translate-y-1 transition-transform duration-300">
            <h3 className="text-xs font-bold tracking-[0.2em] text-accent uppercase mb-6">
              Character Entropy
            </h3>
            <div className="flex flex-col gap-4">
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-textSecondary">Domain</span>
                  <span>{result.entropies?.domain || 0}</span>
                </div>
                <div className="w-full bg-white/5 h-1.5 rounded-full overflow-hidden">
                  <div
                    className="bg-accent h-full"
                    style={{
                      width: `${Math.min(100, (result.entropies?.domain / 5) * 100)}%`,
                    }}
                  ></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-textSecondary">Path</span>
                  <span>{result.entropies?.path || 0}</span>
                </div>
                <div className="w-full bg-white/5 h-1.5 rounded-full overflow-hidden">
                  <div
                    className="bg-glow h-full"
                    style={{
                      width: `${Math.min(100, (result.entropies?.path / 5) * 100)}%`,
                    }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Breakdown & Findings */}
        <div className="lg:col-span-2 flex flex-col gap-8">
          <div className="glass-panel p-8 hover:-translate-y-1 transition-transform duration-300">
            <h2 className="text-xs font-bold tracking-[0.2em] text-accent uppercase mb-6 flex items-center gap-3">
              <Info className="w-4 h-4" /> URL Component Breakdown
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-white/2 p-4 border border-white/5">
                <div className="text-[10px] text-textSecondary uppercase tracking-widest mb-1">
                  Protocol
                </div>
                <div className="font-display text-sm">{result.protocol}</div>
              </div>
              <div className="bg-white/2 p-4 border border-white/5 col-span-2 md:col-span-1 break-all">
                <div className="text-[10px] text-textSecondary uppercase tracking-widest mb-1">
                  Hostname
                </div>
                <div className="font-display text-sm">{result.hostname}</div>
              </div>
              <div className="bg-white/2 p-4 border border-white/5 break-all">
                <div className="text-[10px] text-textSecondary uppercase tracking-widest mb-1">
                  Path
                </div>
                <div className="font-display text-sm">
                  {result.pathname || "/"}
                </div>
              </div>
              <div className="bg-white/2 p-4 border border-white/5 break-all">
                <div className="text-[10px] text-textSecondary uppercase tracking-widest mb-1">
                  Params
                </div>
                <div className="font-display text-sm">
                  {result.searchParams || "None"}
                </div>
              </div>
            </div>
          </div>

          <div className="glass-panel p-10 h-full relative hover:-translate-y-1 transition-transform duration-300">
            <div className="absolute top-0 left-0 w-full h-1 bg-linear-to-r from-transparent via-accent/20 to-transparent"></div>
            <h2 className="text-xs font-bold tracking-[0.2em] text-accent uppercase mb-8 flex items-center gap-3">
              <Shield className="w-4 h-4" /> Triggered Sensors & Explainability
            </h2>

            {result.findings && result.findings.length > 0 ? (
              <div className="flex flex-col gap-5">
                {result.findings.map((finding, idx) => (
                  <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.4 + idx * 0.1 }}
                    key={finding.id}
                    className="bg-white/2 border border-white/5 p-6 rounded flex items-start gap-5 hover:bg-white/4 transition-colors group"
                  >
                    <div
                      className={`mt-1 rounded-sm p-1.5 ${finding.severity === "critical" ? "bg-danger/20 text-danger" : finding.severity === "high" ? "bg-danger/20 text-danger" : "bg-warning/20 text-warning"}`}
                    >
                      <AlertTriangle className="w-4 h-4" />
                    </div>
                    <div className="flex-1">
                      <div className="flex justify-between items-center mb-2">
                        <div className="flex items-center gap-3">
                          <h3 className="font-bold text-sm tracking-widest text-textPrimary uppercase">
                            {finding.name}
                          </h3>
                          <span
                            className={`text-[10px] uppercase tracking-widest px-2 py-0.5 rounded border ${finding.severity === "critical" ? "border-danger text-danger" : "border-warning text-warning"}`}
                          >
                            {finding.severity}
                          </span>
                        </div>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-4">
                        <div className="bg-black/20 p-3 rounded border border-white/5">
                          <div className="text-[10px] text-textSecondary uppercase tracking-widest mb-1">
                            Explanation
                          </div>
                          <p className="text-xs leading-relaxed text-textPrimary/90">
                            {finding.explanation}
                          </p>
                        </div>
                        <div className="bg-black/20 p-3 rounded border border-white/5">
                          <div className="text-[10px] text-textSecondary uppercase tracking-widest mb-1">
                            Evidence Captured
                          </div>
                          <p className="text-xs font-mono text-accent break-all">
                            {finding.evidence || "N/A"}
                          </p>
                        </div>
                      </div>

                      <div className="text-[11px] text-glow/90 bg-glow/10 px-4 py-2.5 rounded inline-block tracking-wider uppercase font-semibold w-full">
                        <span className="text-accent mr-3">
                          RECOMMENDATION:
                        </span>
                        {finding.recommendation}
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center min-h-75 text-center text-textSecondary">
                <CheckCircle className="w-16 h-16 text-success/40 mb-6" />
                <p className="font-bold tracking-[0.2em] text-sm uppercase text-success/80">
                  No anomalies detected
                </p>
                <p className="text-xs mt-3 max-w-sm leading-relaxed text-textSecondary/60">
                  The sensor network did not identify any patterns typically
                  associated with malicious intent or obfuscation.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
}
