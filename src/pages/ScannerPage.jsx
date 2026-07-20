import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { ArrowRight } from "lucide-react";

// Floating particles component
const Particles = () => {
  const [particles, setParticles] = useState([]);

  useEffect(() => {
    const arr = Array.from({ length: 20 }).map((_, i) => ({
      id: i,
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: Math.random() * 3 + 1,
      duration: Math.random() * 20 + 10,
    }));
    setParticles(arr);
  }, []);

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-30">
      {particles.map((p) => (
        <motion.div
          key={p.id}
          className="absolute rounded-full bg-accent"
          style={{
            width: p.size,
            height: p.size,
            left: `${p.x}%`,
            top: `${p.y}%`,
          }}
          animate={{
            y: [0, -100, 0],
            opacity: [0, 1, 0],
          }}
          transition={{
            duration: p.duration,
            repeat: Infinity,
            ease: "linear",
          }}
        />
      ))}
    </div>
  );
};

export default function ScannerPage() {
  const [url, setUrl] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const navigate = useNavigate();

  const handleAnalyze = (e) => {
    e.preventDefault();
    if (!url) return;

    setIsAnalyzing(true);
    setTimeout(() => {
      navigate("/report", { state: { urlToAnalyze: url } });
    }, 1200);
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.2, delayChildren: 0.1 },
    },
    exit: {
      opacity: 0,
      y: -20,
      filter: "blur(10px)",
      transition: { duration: 0.5 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.8, ease: "easeOut" },
    },
  };

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      exit="exit"
      className="flex-1 flex flex-col justify-between relative"
    >
      <Particles />

      <div className="flex-1 flex flex-col items-center justify-center -mt-10 relative z-10">
        <motion.h1
          variants={itemVariants}
          className="text-5xl md:text-7xl font-display font-bold tracking-[0.2em] mb-16 text-center"
          style={{ color: "#c58b7c" }}
        >
          TALES OF TIME
        </motion.h1>

        <motion.form
          variants={itemVariants}
          onSubmit={handleAnalyze}
          className="w-full max-w-2xl relative group"
        >
          <div className="absolute -inset-1 bg-linear-to-r from-accent/10 to-glow/10 rounded-sm blur opacity-0 group-hover:opacity-100 transition duration-1000 group-hover:duration-200"></div>
          <div className="relative flex items-center bg-[#151515]/80 backdrop-blur-sm border border-white/5 rounded-sm overflow-hidden focus-within:border-accent/50 transition-colors shadow-2xl">
            <input
              type="url"
              required
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="ENTER URL FOR HEURISTIC ANALYSIS..."
              className="w-full bg-transparent px-8 py-5 text-sm font-semibold tracking-widest text-white placeholder-textSecondary/40 focus:outline-none"
            />
            <button
              type="submit"
              disabled={isAnalyzing}
              className="bg-accent hover:bg-orange-500 text-[#0d0c0c] px-10 py-5 font-bold text-sm tracking-widest transition-all flex items-center gap-3 h-full relative overflow-hidden group/btn"
            >
              <span className="relative z-10">
                {isAnalyzing ? "ANALYZING..." : "INITIATE"}
              </span>
              {!isAnalyzing && (
                <ArrowRight className="w-4 h-4 relative z-10 group-hover/btn:translate-x-1 transition-transform" />
              )}
              <div className="absolute inset-0 bg-white/20 translate-y-full group-hover/btn:translate-y-0 transition-transform duration-300 ease-out"></div>
            </button>
          </div>
        </motion.form>
      </div>

      <motion.div
        variants={itemVariants}
        className="flex flex-col md:flex-row justify-between items-end gap-8 pb-4 relative z-10"
      >
        <div className="max-w-md">
          <div className="flex items-center gap-4 mb-5">
            <div className="h-px w-12 bg-accent"></div>
            <span className="text-accent text-xs font-bold tracking-[0.2em] uppercase">
              HEURISTIC DETECTION ENGINE 01-A
            </span>
          </div>
          <p className="text-textSecondary text-sm leading-relaxed pr-8 font-medium">
            Deciphering malicious intent through explainable heuristics. Every
            URL parameter, domain token, and character entropy represents a
            potential threat vector.
          </p>
        </div>

        <div className="flex items-end gap-16">
          <div>
            <div className="text-[10px] text-textSecondary uppercase tracking-[0.2em] mb-2 text-right">
              Confidence
            </div>
            <div className="text-xl font-display font-semibold tracking-wide text-white">
              99.9%
            </div>
          </div>
          <div>
            <div className="text-[10px] text-textSecondary uppercase tracking-[0.2em] mb-2 text-right">
              Latency
            </div>
            <div className="text-xl font-display font-semibold tracking-wide text-white">
              12.4 ms
            </div>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}
