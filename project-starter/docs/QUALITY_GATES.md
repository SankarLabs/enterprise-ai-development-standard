# Engineering quality gates

| Gate | Check | Threshold / policy | Evidence | Blocking? |
|---|---|---|---|---|
| Static analysis | Lint / format / type check | Approved rules | CI run | Yes |
| Unit tests | Unit suite | Project-defined | CI run | Yes |
| Integration | Contracts and dependencies | Project-defined | CI run | Risk-based |
| Security | SAST / dependency / secret scan | Company policy | Scan report | Yes per policy |
| Performance | Load / latency | NFR targets | Test report | Risk-based |
| E2E | Critical user journeys | Approved scenarios | Test report | Risk-based |

Never lower a threshold or disable a control to make a build pass without an approved policy change and documented risk acceptance.
