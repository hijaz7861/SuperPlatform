# Execution Policy

The engine may autonomously perform routine, reversible software tasks.

The engine must require explicit approval for:
- destructive deletion outside a disposable workspace
- financial transactions
- credential/key changes
- publishing/deployment to production
- actions affecting third-party systems
- irreversible infrastructure changes

Never expose arbitrary shell execution directly through the public command API.
Use explicit, allow-listed worker actions.
