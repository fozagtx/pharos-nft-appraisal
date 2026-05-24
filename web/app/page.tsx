import Link from "next/link";
import { Nav } from "@/components/Nav";
import { Footer } from "@/components/Footer";
import { ConnectRedirect } from "@/components/ConnectRedirect";
import { HowItWorks } from "@/components/HowItWorks";
import {
  MotionCta,
  MotionFact,
  MotionFacts,
  MotionHeroTitle,
  MotionLede,
} from "@/components/PageMotion";

/* Hallmark · genre: modern-minimal · macrostructure: Marquee Hero · theme: paper-amber
 * H1 Marquee knobs: size=xxl, alignment=left-bias, underlay=rule-below
 * nav: N5 · footer: Ft2 · enrichment: none
 * design-system: design.md · designed-as-app
 */

type TokenKind = "btc" | "musd";

export default function Landing() {
  return (
    <>
      <ConnectRedirect to="/app" />
      <Nav />
      <main className="landing">
        <section className="marquee">
          <MotionHeroTitle>
            Borrow dollars
            <br />
            against your Bitcoin.
          </MotionHeroTitle>
        </section>

        <hr className="rule-thick" aria-hidden />

        <section className="below">
          <MotionLede>
            <p>
              Deposit BTC, borrow MUSD, and repay when ready to release your
              Bitcoin back.
            </p>
          </MotionLede>

          <div className="landing-snapshot" aria-label="Example position">
            <SnapshotItem token="btc" label="Collateral" value="0.001 BTC" />
            <SnapshotItem token="musd" label="Debt" value="2,009.01 MUSD" />
          </div>

          <HowItWorks />

          <MotionFacts>
            <Fact term="Minimum debt" value="1,800 MUSD" note="Per vault, protocol-set." />
            <Fact term="Minimum ICR" value="110%" note="Below this, vaults are liquidatable." />
            <Fact term="Interest" value="1–5% APR" note="Set by InterestRateManager, locked at open." />
            <Fact term="Redemption fee" value="0.75%" note="Charged on BTC released via redemption." />
            <Fact term="Gas token" value="BTC" note="Mezo pays gas natively in BTC." />
            <Fact term="Network" value="Mezo testnet" note="Real testnet, not mock." />
          </MotionFacts>

          <MotionCta>
            <Link href="/app" className="primary-cta">
              Borrow MUSD
            </Link>
          </MotionCta>
        </section>
      </main>
      <Footer />
    </>
  );
}

function SnapshotItem({
  token,
  label,
  value,
}: {
  token: TokenKind;
  label: string;
  value: string;
}) {
  return (
    <div className="snapshot-item">
      <TokenMark kind={token} />
      <span className="snapshot-label">{label}</span>
      <span className="snapshot-value">{value}</span>
    </div>
  );
}

function TokenMark({ kind }: { kind: TokenKind }) {
  return (
    <span className={`token-mark token-mark-${kind}`} aria-hidden="true">
      {kind === "btc" ? "₿" : "M"}
    </span>
  );
}

function Fact({
  term,
  value,
  note,
}: {
  term: string;
  value: string;
  note: string;
}) {
  return (
    <MotionFact>
      <dt>{term}</dt>
      <dd className="value">{value}</dd>
      <dd className="note">{note}</dd>
    </MotionFact>
  );
}
