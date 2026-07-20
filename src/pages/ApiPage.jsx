import { motion } from "framer-motion";
import { Terminal, Copy } from "lucide-react";

export default function ApiPage() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="flex-1 py-8 flex flex-col"
    >
      <div className="flex items-center gap-4 mb-10">
        <Terminal className="w-8 h-8 text-accent" />
        <div>
          <h1 className="text-2xl font-display font-bold tracking-widest uppercase">
            Sensor API
          </h1>
          <p className="text-xs text-textSecondary uppercase tracking-widest mt-1">
            Integrate PhishLens into your pipeline
          </p>
        </div>
      </div>

      <div className="glass-panel p-8 max-w-3xl">
        <h2 className="text-sm font-bold tracking-[0.2em] text-accent uppercase mb-6">
          REST API Endpoint
        </h2>
        <p className="text-sm text-textSecondary mb-6 leading-relaxed">
          The PhishLens heuristic engine is fully stateless and can be deployed
          as an edge function or microservice. Send a POST request to analyze
          URLs programmatically.
        </p>

        <div className="bg-[#0d0c0c] border border-white/10 rounded-md p-4 relative group font-mono text-sm mb-8">
          <button className="absolute top-4 right-4 text-textSecondary hover:text-white transition-colors">
            <Copy className="w-4 h-4" />
          </button>
          <div className="text-accent mb-2">POST /api/v1/analyze</div>
          <div className="text-textSecondary">
            <span className="text-white">Content-Type:</span> application/json
          </div>
          <br />
          <div className="text-success">{`{`}</div>
          <div className="pl-4 text-white">{`"url": "https://secure-login.example.com"`}</div>
          <div className="text-success">{`}`}</div>
        </div>

        <h2 className="text-sm font-bold tracking-[0.2em] text-accent uppercase mb-6">
          Response Format
        </h2>

        <div className="bg-[#0d0c0c] border border-white/10 rounded-md p-4 relative group font-mono text-xs text-textSecondary">
          <pre>
            {`{
  "score": 65,
  "riskLevel": "Suspicious",
  "confidence": "High",
  "entropies": {
    "domain": "4.21",
    "path": "3.50",
    "max": "4.21"
  },
  "findings": [
    {
      "id": "keyword-detector",
      "name": "Deceptive Keywords",
      "severity": "warning",
      "score": 30,
      "evidence": "login, secure"
    }
  ]
}`}
          </pre>
        </div>
      </div>
    </motion.div>
  );
}
