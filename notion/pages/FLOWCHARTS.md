# 🗺️ Workflow Flowcharts

> Visual maps of lead journeys and automations

---

## Lead Journey Flowchart

Copy this into a Notion **Code Block** and select "Mermaid" as the language:

```mermaid
flowchart TD
    subgraph JENNICA["🟣 JENNICA"]
        A[New Lead] -->|Search superlative| B[SMS Sent]
        B -->|No reply 7 days| C[30-Day Timeout]
        C -->|30 days pass| A
    end

    subgraph ANA["🔵 ANA"]
        B -->|They reply!| D[Replied - Awaiting Ana]
        D -->|Respond < 4hrs| E[Ana Engaged]
        E -->|Send resources| F[Tool Offered]
        F -->|They engage| G[Relationship Building]
        F -->|No response 14 days| C
        G -->|Find pain points| H[Ask Made]
        H -->|"Not now"| I[Hibernation 90-Day]
        I -->|90 days pass| A
        H -->|Yes!| J[Meeting Scheduled]
    end

    subgraph DJ["🟢 DJ"]
        J -->|Meet with lead| K[DJ Meeting Complete]
        K -->|Send offer| L[Offer Extended]
        L -->|They sign!| M[Won 🎉]
        L -->|No response| N[Follow-up Cadence]
        N -->|Still no| I
    end

    subgraph LOST["❌ LOST"]
        H -->|"Never"| O[Lost - Not Interested]
        D -->|"Stop texting"| P[Dead - Negative Reply]
        K -->|Bad fit| Q[Lost - Not Qualified]
        L -->|Joined competitor| R[Lost - Competitor]
    end

    style A fill:#9b59b6,color:#fff
    style M fill:#27ae60,color:#fff
    style O fill:#e74c3c,color:#fff
    style P fill:#e74c3c,color:#fff
    style Q fill:#e74c3c,color:#fff
    style R fill:#e74c3c,color:#fff
```

---

## Daily Workflow by Role

Copy this into a Notion **Code Block** and select "Mermaid" as the language:

```mermaid
flowchart LR
    subgraph MORNING["☀️ MORNING"]
        A1[Jennica: Check new leads]
        A2[Ana: Check replies]
        A3[DJ: Check meetings]
    end

    subgraph MIDDAY["🌤️ MIDDAY"]
        B1[Jennica: Send SMS batch]
        B2[Ana: Follow up on tools]
        B3[DJ: Send offers]
    end

    subgraph AFTERNOON["🌅 AFTERNOON"]
        C1[Jennica: Log activity]
        C2[Ana: Make asks]
        C3[DJ: Follow-up calls]
    end

    A1 --> B1 --> C1
    A2 --> B2 --> C2
    A3 --> B3 --> C3
```

---

## Handoff Points

Copy this into a Notion **Code Block** and select "Mermaid" as the language:

```mermaid
flowchart LR
    J[🟣 Jennica] -->|"Lead replies"| A[🔵 Ana]
    A -->|"Meeting scheduled"| D[🟢 DJ]
    D -->|"No show"| A
    D -->|"Needs nurture"| A

    style J fill:#9b59b6,color:#fff
    style A fill:#3498db,color:#fff
    style D fill:#27ae60,color:#fff
```

**Handoff Triggers:**
| From | To | Trigger |
|------|-----|---------|
| Jennica → Ana | Lead replies to SMS |
| Ana → DJ | Meeting scheduled |
| DJ → Ana | No-show (reschedule) |
| DJ → Ana | Needs more nurturing |

---

## Automation Map

Copy this into a Notion **Code Block** and select "Mermaid" as the language:

```mermaid
flowchart TD
    subgraph AUTOMATIC["⚡ AUTOMATIC"]
        T1[New Lead Created] -->|Monday| T2[Temperature = Cold]
        T1 -->|Monday| T3[First Contact Date = Today]
        T1 -->|Make.com| T4[Create CRM Contact]
        T1 -->|Make.com| T5[Check for Duplicates]

        S1[Status Changes] -->|Monday| S2[Update Temperature]
        S1 -->|Monday| S3[Stage Entry Date = Today]
        S1 -->|Monday| S4[Notify Team via Slack]

        W1[Status = Won] -->|Make.com| W2[Create CRM Deal]
        W1 -->|Monday| W3[Notify DJ]
    end

    subgraph MANUAL["👤 MANUAL"]
        M1[Search Courted for superlative]
        M2[Personalize SMS message]
        M3[Update Next Action]
        M4[Log call notes]
        M5[Schedule meeting]
    end

    style T1 fill:#3498db,color:#fff
    style S1 fill:#3498db,color:#fff
    style W1 fill:#27ae60,color:#fff
```

---

## Status Decision Tree

Copy this into a Notion **Code Block** and select "Mermaid" as the language:

```mermaid
flowchart TD
    Q1{Did they reply?}
    Q1 -->|Yes| R1[Replied - Awaiting Ana]
    Q1 -->|No 7+ days| R2[30-Day Timeout]
    Q1 -->|Said STOP| R3[Dead - Negative Reply]

    R1 --> Q2{Engaged after tools?}
    Q2 -->|Yes| R4[Relationship Building]
    Q2 -->|No 14+ days| R2

    R4 --> Q3{Said yes to meeting?}
    Q3 -->|Yes| R5[Meeting Scheduled]
    Q3 -->|Not now| R6[Hibernation 90-Day]
    Q3 -->|Never| R7[Lost - Not Interested]

    R5 --> Q4{Meeting outcome?}
    Q4 -->|Good fit| R8[Offer Extended]
    Q4 -->|No show| R9[No Show]
    Q4 -->|Bad fit| R10[Lost - Not Qualified]

    R8 --> Q5{Did they sign?}
    Q5 -->|Yes!| R11[Won 🎉]
    Q5 -->|Joined competitor| R12[Lost - Competitor]
    Q5 -->|No response| R6

    style R11 fill:#27ae60,color:#fff
    style R3 fill:#e74c3c,color:#fff
    style R7 fill:#e74c3c,color:#fff
    style R10 fill:#e74c3c,color:#fff
    style R12 fill:#e74c3c,color:#fff
```

---

## How to Add to Notion

1. Create a new page called **🗺️ Workflow Flowcharts**
2. For each flowchart above:
   - Type `/code` and press Enter
   - Select **Mermaid** as the language
   - Paste the code between the triple backticks
3. The flowchart will render automatically!

---

## Quick Reference: Status Colors

| Color | Owner | Statuses |
|-------|-------|----------|
| 🟣 Purple | Jennica | New Lead, SMS Sent |
| 🔵 Blue | Ana | Replied through Meeting Scheduled |
| 🟢 Green | DJ | DJ Meeting Complete through Won |
| 🟡 Yellow | System | Timeout, Hibernation, No Show |
| 🔴 Red | Terminal | All Lost/Dead statuses |
