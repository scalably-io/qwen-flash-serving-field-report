# Historical coverage, October 5, 2026

The requested complete per-engine tuning/stress matrix remains incomplete. PASS applies only to the stated cells. PARTIAL is unfinished measurement; INVALID is contaminated evidence excluded from conclusions.

| Profile | API | 256K output | Other gate |
|---|---|---|---|
| Frozen EXL | Tools/schema/history PASS | Cold/warm PASS | Earlier parking/churn PASS; final parked repeat PARTIAL |
| Tuned EXL | Tools/schema/history PASS | Cold/warm PASS | Overload fairness FAIL, 226.34s short-probe TTFT |
| Strata serial | Tools/schema/history PASS | C1 cold/warm PASS | Native batch C4/C5 FAIL; serial mixed NOT RUN; overload PARTIAL |
| NInfer-ext | Named forced tools/schema unsupported | Cold PASS; warm PARTIAL | One GPU; 100K C5 had allocation failures |
| FreeToken | Tools/history PASS; schema unsupported | PARTIAL; warm NOT RUN | One GPU; tested TP2 expert kernels unsupported |
| Stock llama.cpp | Required API PASS | Cold PASS; warm PARTIAL | Clean four-slot memory gate FAIL; stress PARTIAL |
| BeeLlama | Required API PASS | Cold PASS; warm PARTIAL | Clean four-slot memory gate FAIL; stress PARTIAL |
| IK storage bridge | Tools/schema/history PASS on compatible converted artifact | Incomplete; warm NOT RUN | Original storage type unsupported; conversion adds 7.08GB; no quality-equivalence proof |

Earlier stock/Bee/IK OOM attempts with a leftover NInfer process are INVALID. Clean retries remain separate. No task-quality score or production replacement was performed.
