"use client";

import { motion, useReducedMotion, type Variants } from "framer-motion";
import type { ReactNode } from "react";

const easeOut = [0.22, 1, 0.36, 1] as const;

const fadeUp: Variants = {
  hidden: { opacity: 0, y: 18, filter: "blur(6px)" },
  show: { opacity: 1, y: 0, filter: "blur(0px)" },
};

const stagger: Variants = {
  hidden: {},
  show: {
    transition: {
      staggerChildren: 0.08,
      delayChildren: 0.08,
    },
  },
};

function motionProps(reduceMotion: boolean, delay = 0) {
  if (reduceMotion) {
    return {
      initial: false,
      animate: { opacity: 1 },
      transition: { duration: 0 },
    };
  }

  return {
    initial: "hidden" as const,
    animate: "show" as const,
    variants: fadeUp,
    transition: { duration: 0.55, delay, ease: easeOut },
  };
}

export function MotionHeroTitle({ children }: { children: ReactNode }) {
  const reduceMotion = useReducedMotion();

  return (
    <motion.h1 className="display" {...motionProps(Boolean(reduceMotion))}>
      {children}
    </motion.h1>
  );
}

export function MotionLede({ children }: { children: ReactNode }) {
  const reduceMotion = useReducedMotion();

  return (
    <motion.div className="lede" {...motionProps(Boolean(reduceMotion), 0.08)}>
      {children}
    </motion.div>
  );
}

export function MotionFacts({ children }: { children: ReactNode }) {
  const reduceMotion = useReducedMotion();

  return (
    <motion.dl
      className="facts"
      initial={reduceMotion ? false : "hidden"}
      whileInView={reduceMotion ? undefined : "show"}
      viewport={{ once: true, amount: 0.2 }}
      variants={stagger}
    >
      {children}
    </motion.dl>
  );
}

export function MotionFact({ children }: { children: ReactNode }) {
  const reduceMotion = useReducedMotion();

  return (
    <motion.div
      className="fact"
      variants={reduceMotion ? undefined : fadeUp}
      transition={{ duration: 0.42, ease: easeOut }}
    >
      {children}
    </motion.div>
  );
}

export function MotionCta({ children }: { children: ReactNode }) {
  const reduceMotion = useReducedMotion();

  return (
    <motion.div className="cta-row" {...motionProps(Boolean(reduceMotion), 0.14)}>
      {children}
    </motion.div>
  );
}

export function MotionWorkbench({ children }: { children: ReactNode }) {
  const reduceMotion = useReducedMotion();

  return (
    <motion.main className="workbench" {...motionProps(Boolean(reduceMotion))}>
      {children}
    </motion.main>
  );
}

export function MotionWorkbenchGrid({ children }: { children: ReactNode }) {
  const reduceMotion = useReducedMotion();

  return (
    <motion.div
      className="workbench-grid"
      initial={reduceMotion ? false : "hidden"}
      animate={reduceMotion ? undefined : "show"}
      variants={stagger}
    >
      {children}
    </motion.div>
  );
}

export function MotionAside({ children }: { children: ReactNode }) {
  const reduceMotion = useReducedMotion();

  return (
    <motion.aside
      variants={reduceMotion ? undefined : fadeUp}
      transition={{ duration: 0.45, ease: easeOut }}
    >
      {children}
    </motion.aside>
  );
}

export function MotionSection({ children }: { children: ReactNode }) {
  const reduceMotion = useReducedMotion();

  return (
    <motion.section
      variants={reduceMotion ? undefined : fadeUp}
      transition={{ duration: 0.45, ease: easeOut }}
    >
      {children}
    </motion.section>
  );
}
