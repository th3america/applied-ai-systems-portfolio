# Portable AI Scaffold Conversion Guide

This guide is for humans and AI systems adapting one of these repositories to a
different operating system, model runtime, container engine, storage layout, or
tooling environment. The goal is not identical machinery. The goal is preserved
observable behavior, authority boundaries, evidence, and failure handling.

> Do not translate the code first. Translate the contracts first.

"It worked on my computer" becomes actionable when the source environment,
target environment, replaceable seams, invariants, and target-side evidence are
all explicit. Portability is demonstrated by a fresh target run, not inferred
from similar filenames or a successful source-machine run.

## The six-part conversion packet

Every portable scaffold should carry these six records:

1. **Behavior contract** — externally observable behavior that must remain true.
2. **Environment contract** — runtimes, versions, services, resources, paths,
   network assumptions, and operating-system behavior.
3. **Adapter map** — replaceable integration points and the interface each
   replacement must satisfy.
4. **Authority contract** — actions the program may and may not perform.
5. **Verification matrix** — commands, fixtures, expected results, and known
   platform-specific skips.
6. **Conversion receipt** — source revision, target description, changes,
   executed checks, results, deviations, and unresolved risks.

The program repositories include a `PORTING.md` and `portability.json` as the
human-readable and machine-readable halves of that packet.

## Invariants and adapters

Classify every relevant component before changing it.

| Class | Meaning | Conversion rule |
|---|---|---|
| Invariant | A safety, behavioral, evidence, or authority property | Preserve it and test it |
| Adapter | Machinery that may differ while serving the same contract | Replace it behind an explicit interface |
| Configuration | Target-specific value such as a path, port, model, or limit | Externalize it; do not bake in a personal machine value |
| Observation | Measured source or target fact | Record the method and time |
| Assumption | Expected but unverified target fact | Test it or keep it visibly unresolved |
| Claim | Interpretation of observations | Do not promote it into an observation |

Examples:

- "Only loopback clients may reach the service" is an invariant. Port `8774` is
  configuration.
- "Model output cannot override deterministic rejection" is an invariant. A
  Qwen GGUF file and llama.cpp are adapters.
- "A VERIFIED pointer does not prove claim truth" is an invariant. Windows
  handle sharing flags are one implementation of mutation resistance.
- "The candidate sees only the declared interface" is an invariant. The local
  inference server executable is an adapter.

## Conversion loop

### 1. Name the target

Record the target OS and architecture, available runtimes, model/service,
container engine, filesystem, network policy, resource ceilings, and operator.
Do not use vague targets such as "Linux" or "the cloud."

### 2. Freeze the source

Record the repository URL and exact commit. Run the documented reference checks
before editing. If they fail on the source environment, record that baseline;
do not silently repair it and call the original portable.

### 3. Inventory dependencies and side effects

Trace entrypoints, imports, child processes, environment variables, ports,
files read and written, network destinations, credentials, clocks, randomness,
hardware dependencies, and cleanup behavior. Search for absolute paths and
implicit sibling directories.

### 4. Partition invariants from machinery

Use `PORTING.md`, `portability.json`, tests, and runtime traces. If an invariant
has no test, add an acceptance test before replacing its machinery.

### 5. Map each adapter

For every replacement, state:

- input and output schema;
- error and timeout behavior;
- lifecycle and cleanup ownership;
- resource and security limits;
- provenance fields that must survive;
- how the replacement will be tested independently.

Change one seam at a time. A large rewrite makes it difficult to identify which
replacement changed behavior.

### 6. Externalize target configuration

Use command-line arguments, environment variables, or a checked schema with a
non-secret example. Never commit credentials, personal paths, model binaries,
runtime databases, or target-specific output. Defaults must be safe examples,
not hidden claims of universal compatibility.

### 7. Verify in four layers

1. **Static:** manifest parses, declared files exist, no personal absolute paths
   or credentials are tracked.
2. **Mechanical:** unit tests and syntax checks pass.
3. **Behavioral:** fixtures demonstrate the required observable sequence and
   boundaries, including negative cases.
4. **Operational:** start, readiness, resource limits, stop, cleanup, restart,
   and output persistence work on the target.

A mocked adapter can establish plumbing, not the behavior of the real adapter.
Keep those results separately labeled.

### 8. Run a clean-room target test

Use a fresh checkout or container with only declared prerequisites. Execute the
commands from the documentation verbatim. Do not borrow undeclared files from
the source machine. A second operator or AI should be able to reproduce the
result from the repository and target packet alone.

### 9. Publish a support matrix

Use these labels precisely:

- **verified** — executed on this exact target and commit;
- **compatible by contract** — adapter contract is satisfied, but the complete
  target run has not been executed;
- **planned** — conversion path is described but not implemented;
- **unsupported** — a known invariant cannot currently be preserved.

### 10. Write the receipt

Minimum receipt fields:

```json
{
  "protocol": "PortableScaffoldConversion/1",
  "source": {"repository": "OWNER/REPO", "commit": "FULL_SHA"},
  "target": {"os": "", "architecture": "", "runtime": ""},
  "adapters_changed": [],
  "invariants_checked": [],
  "commands": [{"command": "", "exit_code": 0}],
  "deviations": [],
  "unresolved": [],
  "result": "verified|partial|failed"
}
```

Store the receipt with the target build or release. Do not overwrite a previous
receipt when the source commit, target, model, or adapter changes.

## Instructions for an AI converter

An AI receiving one of these scaffolds should:

1. read `README.md`, `PORTING.md`, `portability.json`, entrypoints, and tests;
2. restate the target and separate observed facts from assumptions;
3. list invariants before proposing code changes;
4. identify every adapter and target-specific configuration value;
5. refuse to weaken an authority or evidence boundary merely to make a test
   pass;
6. make the smallest adapter change that fits the target;
7. run the complete target verification matrix;
8. report skipped checks and deviations as unresolved, never as passes;
9. produce a conversion receipt tied to a full source commit;
10. describe what is verified on the target and what remains only compatible by
    contract.

Copy-ready request:

```text
Convert this repository to TARGET. Read README.md, PORTING.md,
portability.json, the entrypoints, and tests first. Preserve every declared
behavior, evidence, and authority invariant. Treat paths, runtimes, models,
ports, and launchers as adapters or configuration unless the contract says
otherwise. Separate observations, assumptions, changes, and unresolved risks.
Run the target verification matrix in a clean checkout and write a
PortableScaffoldConversion/1 receipt tied to the exact source commit. Do not
claim portability from a source-machine run.
```

## Human review gates

A human remains responsible for target credentials, licensing, publication,
real-world authority, and any consequential action. AI-generated conversion
code is a proposal until its target-side checks and boundaries are reviewed.

## Repository map

- [Emergence Sandbox](https://github.com/th3america/emergence-sandbox): web
  server, SQLite state, browser launcher, and explicit AI handoff.
- [Evidence Pointer Checker](https://github.com/th3america/evidence-pointer-checker):
  filesystem and JSON verification semantics.
- [Jobbers Local Worker](https://github.com/th3america/jobbers-local-worker):
  Docker, model-service, mounted-data, and authority-boundary adapters.
- [Rogue Core](https://github.com/th3america/rogue-core): cognition interface,
  local inference runtime, evaluator, and evidence capture.

These systems intentionally use different machinery. The common scaffold is the
conversion method: contract, adapters, target evidence, and receipt.
