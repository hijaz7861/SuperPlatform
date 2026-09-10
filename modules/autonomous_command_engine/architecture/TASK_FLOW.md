# Autonomous Task Flow

1. Receive one natural-language command.
2. Classify it into a controlled task type.
3. Estimate CPU/GPU/quantum/storage requirements.
4. Select an available worker.
5. Execute the task.
6. Verify the result.
7. If a supported repair strategy exists, apply it and retest.
8. Store logs and result.
9. Return the final status to Termux.

Provider adapters should implement a common interface:

- health()
- capabilities()
- submit(job)
- status(job_id)
- cancel(job_id)
- fetch_result(job_id)

Future adapters:
- CPU worker
- GPU worker
- quantum simulator
- real quantum hardware API
- remote build worker
- OCR worker
