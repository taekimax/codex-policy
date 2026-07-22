# Decisions

Append decision records below. Do not rewrite prior decisions unless correcting a factual error.

## Decision Record

- Date: 2026-07-22
- Decision: Treat Loop Init as an explicitly managed, opt-in reviewed user skill, not a global mandatory workflow.
- Reason: Durable state is useful for extended work, but mandatory roles and artifact creation conflict with the policy’s smallest-effective-support rule.
- Alternatives Considered: Leave the runtime skill unmanaged; add it as a retained system skill; apply it implicitly for ordinary repository tasks.
- Reversal Condition: Reconsider only with evidence that an expanded default is needed and does not create policy conflicts.

- Date: 2026-07-22
- Decision: Let global policy select Loop Init for read-only inspection of suitable new-repository work, but retain user confirmation as the only authority for initialization.
- Reason: This makes durable continuation available without turning every new repository or small task into a mandatory workflow.
- Alternatives Considered: Keep explicit user invocation as the only trigger; automatically apply Loop Init to every new repository.
- Reversal Condition: Reconsider if policy-triggered inspection proves noisy or agents cannot reliably distinguish durable work from small tasks.
