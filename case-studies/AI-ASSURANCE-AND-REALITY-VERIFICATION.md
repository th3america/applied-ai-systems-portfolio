# Case study: AI assurance and Reality Verification

## Problem

Language models can produce explanations that sound internally consistent even
when the claimed work did not occur, the evidence does not support it, or the
system silently changed the scope of the claim.

## Architecture

Jason designed a behavior-first verification approach that separates:

1. whether a claimed outcome resolves against observable evidence; and
2. how well the outcome performs, considered only after resolution.

The implementation work adds source hashes, exact locators, preserved inputs,
attributed reviews, uncertainty, counterarguments, stopping conditions, and
separate receipts. File agreement remains evidence about bytes and locations;
it does not automatically establish universal truth or grant authority.

## Professional relevance

This maps directly to AI assurance, model-risk evaluation, auditability,
responsible AI, safety cases, evidence-chain engineering, and evaluation design.
