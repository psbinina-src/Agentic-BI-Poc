# Phase 3 Commands — Prompt-Driven Gold Data Intelligence

Run commands from the repository root in PowerShell.

## 1. Install Phase 3 Dependencies

```powershell
py -m pip install -e ".[test,phase3]"
```

## 2. Configure the OpenAI Key Locally

For this local synthetic-data PoC, the root `.env` contains the key you asked to use. It was exposed in chat, so treat it as compromised and do not reuse it outside this PoC; rotate it when practical. The app reads the ignored `.env` file at startup. Never commit the file or paste the key into chat.

Alternatively, in the PowerShell terminal that will start the Phase 3 server, set the key for this shell session using a hidden prompt:

```powershell
$secureKey = Read-Host "Enter newly rotated OpenAI API key" -AsSecureString
$keyPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureKey)
try {
	$env:OPENAI_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($keyPointer)
}
finally {
	[Runtime.InteropServices.Marshal]::ZeroFreeBSTR($keyPointer)
	Remove-Variable secureKey, keyPointer
}
```

The value is not echoed or stored in shell history and is available only to that PowerShell process and child processes. Start Phase 3 from the same terminal. Never paste the key into chat, commit it, or put it in a tracked file.

Optional configuration:
- `OPENAI_MODEL` (default: `gpt-4o-mini`)
- `PHASE2_API_URL` (default: `http://127.0.0.1:8100`)

## 3. Start Phase 2 (Terminal 1)

In its own terminal, start the Gold REST API on loopback using the command in [Phase 2 commands](../phase-2/phase-2-commands.md). Phase 3 calls its catalogue, schema, and query endpoints; Phase 2 must be running before analysis requests.

## 4. Start Phase 3 Dashboard (Terminal 2)

After configuring `.env`, start Phase 3 so it loads the settings:

```powershell
py -m uvicorn p3_agent.api:app --app-dir src --host 127.0.0.1 --port 8200
```

Open `http://127.0.0.1:8200/`. Keep the host at `127.0.0.1`; do not expose the PoC to the network. Stop each server with `Ctrl+C` when done.

## 5. Check Health and API Contract

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8200/health'
$body = @{ question = "Show net sales by customer region" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:8200/api/ask' -ContentType 'application/json' -Body $body
```

The response contains `answer`, `insight`, `chart`, and `data`. OpenAPI documentation is at `http://127.0.0.1:8200/docs` while the service is running.

## 6. Run Tests

```powershell
py -m pytest tests/p3 -q
py -m pytest -q
```

Tests mock OpenAI and Phase 2 HTTP responses. Live prompt analysis requires a valid, newly rotated key plus the Phase 2 service running.

For manual testing, use the five prompts in [Phase 3 test prompts](phase-3-test-prompts.md). Start with the first prompt to verify the full prompt-to-Gold-to-chart path.
