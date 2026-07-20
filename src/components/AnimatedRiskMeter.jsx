import { motion } from "framer-motion";

export function AnimatedRiskMeter({ score }) {
  const percentage = Math.min(100, Math.max(0, score));

  // Calculate color based on score
  let color = "#33d69f"; // success
  if (score >= 40) color = "#f59e0b"; // warning
  if (score >= 75) color = "#ef4444"; // danger

  return (
    <div className="relative w-64 h-32 flex flex-col items-center justify-end overflow-hidden mt-8">
      {/* Background Arc */}
      <div className="absolute top-0 w-64 h-64 rounded-full border-20 border-white/5 border-b-transparent border-r-transparent rotate-45 transform origin-center"></div>

      {/* Colored Score Arc */}
      <motion.div
        initial={{ rotate: -135 }}
        animate={{ rotate: -135 + percentage * 1.8 }} // 180 degrees total
        transition={{ duration: 1.5, ease: "easeOut", delay: 0.5 }}
        className="absolute top-0 w-64 h-64 rounded-full border-20 border-b-transparent border-r-transparent transform origin-center"
        style={{ borderColor: color }}
      />

      {/* Score Text */}
      <div className="absolute bottom-0 flex flex-col items-center">
        <motion.span
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 1 }}
          className="text-5xl font-display font-bold text-glow"
          style={{ color }}
        >
          {score}
        </motion.span>
        <span className="text-textSecondary text-xs uppercase tracking-widest mt-1 font-semibold">
          Risk Score
        </span>
      </div>
    </div>
  );
}
