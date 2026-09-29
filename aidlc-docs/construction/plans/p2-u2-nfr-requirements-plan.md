# P2-U2 NFR Requirements Plan — Local Service Access

## Context
- Functional Design for P2-U2 is approved; see `aidlc-docs/construction/p2-u2/functional-design/`.
- Keep the NFR assessment small: one local data engineer, synthetic local data, no production SLA/HA target, no container or hosted runtime.
- Required baseline: `CUBEJS_DEV_MODE=false`, authenticated Cube REST, authenticated Cube SQL when enabled, local secrets only, read-only MCP with bounded results.
- Known issue: Cube Core 1.7.47 binds REST/SQL listeners to wildcard addresses. The inspected workstation currently has enabled firewall profiles with default inbound block and no Node/Cube inbound allow rule; keep production auth enabled and recheck this policy before runs.

## Assessment Checklist
- [x] Select the local exposure policy: production mode/authenticated APIs plus existing Windows Firewall inbound-block defaults. Verify no Node/Cube inbound allow exists, deny any future Node allow prompt, and stop if policy changes. No firewall modifications are needed under the inspected current policy.
- [x] Define the minimum auth/secret requirements for REST, SQL, and MCP-to-REST calls.
- [x] Record no additional response-time, throughput, availability, DR, or scaling targets for this PoC.
- [x] Generate concise `nfr-requirements.md` and `tech-stack-decisions.md`.
- [x] Preserve Cube Core, DuckDB, native process, and no-container requirements.

## Question 1: Local listener network boundary
Cube 1.7.47 listens on wildcard interfaces by default; production mode supports JWT for REST and SQL credentials, but authentication alone does not make the listeners loopback-only. Which minimal boundary should P2-U2 require?

A) Keep Cube in authenticated production mode and rely on the existing enabled Windows Defender Firewall inbound-block defaults after confirming no Node/Cube inbound allow exists. Deny any Windows prompt to allow Node inbound; no new firewall rule/admin change. Recheck profiles and rules before each run. (Recommended; simplest for this PoC.)

B) Allow access from the trusted private LAN with production authentication. This relaxes the approved local-only/loopback intent and requires changing the requirements before implementation.

X) Other (please describe after [Answer]: tag below)

[Answer]: A — use production mode/authenticated APIs; verify the existing inbound-block defaults and absence of Node/Cube allow rules; deny any Node firewall prompt; stop if policy changes.

## Review Gate
**Approved** by the user on 2026-09-30: "approved go ahead, just do quick develolpment of rest fast". NFR Requirements are approved. The inspected host firewall meets the basic PoC boundary without modifications; continue to NFR Design and preserve production-mode authentication and deny-on-prompt behavior.
