"use client";

import { useEffect, useState } from "react";
import type { CSSProperties } from "react";
import { Modal } from "@/components/Modal";

const STORAGE_KEY = "mezocircles:getting-started-seen";

const steps = [
  {
    title: "Connect",
    detail: "Use the vault owner wallet.",
  },
  {
    title: "Open",
    detail: "Deposit BTC, borrow at least 1,800 MUSD.",
  },
  {
    title: "Manage",
    detail: "Watch ICR, add BTC, repay, or close.",
  },
] as const;

export function GettingStartedGuide() {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    let shouldOpen = false;
    try {
      if (!window.localStorage.getItem(STORAGE_KEY)) {
        window.localStorage.setItem(STORAGE_KEY, "1");
        shouldOpen = true;
      }
    } catch {
      shouldOpen = true;
    }

    if (!shouldOpen) return;
    const id = window.setTimeout(() => setOpen(true), 0);
    return () => window.clearTimeout(id);
  }, []);

  return (
    <>
      <button
        type="button"
        className="dashboard-demo-trigger"
        aria-haspopup="dialog"
        onClick={() => setOpen(true)}
      >
        <span className="dashboard-demo-dot" aria-hidden="true" />
        <span>Demo</span>
      </button>

      <Modal
        open={open}
        onClose={() => setOpen(false)}
        title="Demo"
      >
        <div className="guide-flow" aria-hidden="true">
          <span />
          <span />
          <span />
        </div>
        <ol className="guide-steps">
          {steps.map((step, index) => (
            <li key={step.title} style={{ "--guide-step": index } as CSSProperties}>
              <span className="guide-step-index">{index + 1}</span>
              <div>
                <strong>{step.title}</strong>
                <p>{step.detail}</p>
              </div>
            </li>
          ))}
        </ol>
        <button
          type="button"
          className="guide-primary"
          onClick={() => setOpen(false)}
        >
          Got it
        </button>
      </Modal>
    </>
  );
}
