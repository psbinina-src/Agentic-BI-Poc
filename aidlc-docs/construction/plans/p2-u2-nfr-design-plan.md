# P2-U2 NFR Design Plan — Basic Local PoC

## Approved NFR Baseline
- Production-mode Cube only: `CUBEJS_DEV_MODE=false`; authenticated REST/SQL; local-only secrets.
- Rely on the already enabled Windows Defender Firewall inbound-block default. Do not add a Node/Cube inbound allow rule. If a Windows prompt requests inbound Node access, deny it. Recheck before service start and stop if policy changes.
- MCP is a local stdio process, read-only, public-member validated, default 100 rows / maximum 500.
- One native local Cube process; no Docker, WSL, hosted service, HA, DR, SLA, or monitoring stack.
- Current measured firewall context: all profiles enabled with `BlockInbound,AllowOutbound`; no explicit Node/Cube inbound allow rule found; local allow rules are GPO managed. No firewall settings will be modified by the app.

## Design Steps
- [x] Map production-mode auth and local secret handling to Cube and MCP configuration.
- [x] Define simple startup preflight: confirm firewall defaults, no Node/Cube inbound allow, no Node inbound prompt accepted; stop if any check fails.
- [x] Define query controls: MCP member allowlist, shape validation, default 100 / hard 500 limit, no SQL text.
- [x] Keep runtime to one Cube native process plus stdio MCP when implemented; use in-memory cache and no Cube Store dependency.
- [x] Confirm no numeric performance/availability target and no background service.
- [x] Validate no new infrastructure or admin firewall changes are included.
- [x] Generate `nfr-design-patterns.md` and `logical-components.md` for review.

## Design Result
NFR design uses the existing managed workstation policy as the control. It does not edit Windows Firewall or claim Cube binds to loopback. Cube remains authenticated and must not be allowed inbound by Windows Firewall. If policy cannot be verified at startup, the local service must not start.

## Review Status
Approved by the user on 2026-09-30: "Approved". Proceed to P2-U2 Code Generation planning, prioritizing local REST first.
