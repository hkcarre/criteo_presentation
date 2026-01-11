# QA Report: Data Logic & Strategic Challenges

## 1. Deep-Dive: Client 31782 Anomaly
**User Query:** *"The clicks have increased... however the estimated revenue lost decreased. Do we have calculations wrong?"*

**Investigation Result:**
*   **Formula Check:** The calculation in the CSV is **Mathematically Correct**.
    *   `Competitor Clicks` * `Revenue Per Click` matches the `Estimated Revenue Lost` column exactly.
*   **The Root Cause (Data Artifact):**
    *   **2023:** Client had high Criteo spend (RPC ~€90-140) + High Competitor Clicks (~700k).
        *   *Result:* Huge Est. Revenue Lost (€50M—€100M/month).
    *   **2024:** The client likely **stopped spending with Criteo** (Churned).
        *   `Revenue Per Click` crashed to **€0.01 - €0.05** (essentially zero).
        *   `Competitor Clicks` **doubled** to ~1.5M/month.
        *   *Result:* `1.5M clicks * €0.01` = **Negligible Revenue Lost (€12k)**.

**Strategic Challenge / Recommendation:**
> **The current metric triggers a paradox:** When we *completely* lose a client (Revenue -> 0), the "Estimated Revenue Lost" metric drops to zero, signaling "No Risk."
>
> **Proposal:** We must recalculate risk using **TRAILING 12-MONTH RPC** (or specific 2023 avg) rather than "Current Month RPC". This would correctly flag Client 31782 as a **€150M+ loss risk** rather than a €12k nuisance.

---

## 2. Sector Evolution (2022 - 2024)
**User Query:** *"Evolution by unique client id and sector... by month and year?"*

Aggregating by **Vertical**, we see a massive shift in the threat landscape.

### 🚨 The "Travel Services" Explosion
Travel was a minor issue in 2022/2023 but has exploded in 2024, becoming our #1 threat vector.
*   **2022:** €113k Lost
*   **2023:** €143k Lost
*   **2024:** **€146,819,300 Lost (1000x Increase)**

### 📉 Classifieds & Real Estate (Stabilizing?)
This was the primary bleeder in 2023 but appears to be cooling off (or suffering the same "Low RPC" data artifact as Client 31782).
*   **2023:** €780M Lost
*   **2024:** €189M Lost

### 📉 Fashion & Retail (Legacy Integrity)
Competitor activity is high (high clicks), but Criteo retains value (RPC remains stable), leading to lower "Lost Revenue" estimates.
*   Fashion 2023: €40M Lost
*   Fashion 2024: €10M Lost

---

## 3. Next Steps
Based on these findings, I recommend adding a **"Data Logic & Caveats"** slide or speaking point to the presentation:
1.  **Acknowledge the "Churn Logic Gap":** Explain that current metrics underestimate risk for fully-churned clients.
2.  **Highlight the Travel Surge:** Ensure the "Travel" vertical is flagged as the new P1 crisis, confirming the "Trip Intent" competitor advantage mentioned in the qualitative slides.
3.  **Update "Revenue at Risk":** If we use the "Historical RPC" logic, the total "Revenue at Risk" number (Slide 7) would likely be **significantly higher** than €39.5M.
