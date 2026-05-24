"use client";

import Link from "next/link";
import { ConnectKitButton } from "connectkit";
import { motion, useReducedMotion, useScroll, useTransform } from "framer-motion";

export function Nav() {
  const reduceMotion = useReducedMotion();
  const { scrollY } = useScroll();
  const navY = useTransform(scrollY, [0, 140], [0, -4]);
  const navScale = useTransform(scrollY, [0, 140], [1, 0.985]);
  const navShadow = useTransform(
    scrollY,
    [0, 140],
    [
      "0 8px 24px -12px oklch(0% 0 0 / 0.10)",
      "0 18px 38px -22px oklch(0% 0 0 / 0.28)",
    ],
  );

  return (
    <motion.nav
      aria-label="Primary"
      className="nav-pill"
      initial={reduceMotion ? false : { opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: reduceMotion ? 0 : 0.4, ease: [0.22, 1, 0.36, 1] }}
      style={
        reduceMotion
          ? undefined
          : {
              y: navY,
              scale: navScale,
              boxShadow: navShadow,
            }
      }
    >
      <Link href="/" className="wordmark">
        mezoCircles
      </Link>
      <Link href="/app" className="nav-link">
        Borrow
      </Link>
      <ConnectKitButton.Custom>
        {({ isConnected, show, truncatedAddress }) => (
          <button type="button" onClick={show} className="cta-fill">
            {isConnected ? truncatedAddress : "Connect wallet"}
          </button>
        )}
      </ConnectKitButton.Custom>
    </motion.nav>
  );
}
