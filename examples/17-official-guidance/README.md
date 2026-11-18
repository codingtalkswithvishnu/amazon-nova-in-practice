# Official AWS guidance — application worksheet

Companion for Chapter 17. This chapter consolidates official-source guidance and
links back to the runnable examples instead of introducing another framework.

1. Record one task, an accepted result and a fixed set of fictional inputs.
2. Name the exact model/profile, generation, API, Region and lifecycle source.
3. Compare a precise prompt with the baseline on the same cases. Keep examples
   used in the prompt separate from the held-out evaluation set.
4. Inspect stop reasons and validate the schema, tool name, arguments and source facts.
5. For a difficult case, change only the relevant prompt, retrieval or reasoning
   setting, then measure quality, failure count, latency and usage again.
6. Save the prompt, source/data version, code commit and reviewer outcome.

[referral-prompt.txt](referral-prompt.txt) is a fictional prompt fragment. It is not
a clinical policy or a complete extraction program. Use the validated Chapter 5
source to apply and check an extraction schema.

Official sources:

- [Nova 1 prompting](https://docs.aws.amazon.com/nova/latest/userguide/prompting.html)
- [Nova 2 precise prompts](https://docs.aws.amazon.com/nova/latest/nova2-userguide/create-precise-prompts.html)
- [Nova 2 examples](https://docs.aws.amazon.com/nova/latest/nova2-userguide/prompting-provide-examples.html)
- [Nova 2 advanced techniques](https://docs.aws.amazon.com/nova/latest/nova2-userguide/advanced-prompting-techniques.html)
- [Nova tool use](https://docs.aws.amazon.com/nova/latest/userguide/tool-use.html)
- [AWS migration guidance](https://aws.amazon.com/blogs/machine-learning/migrate-from-amazon-nova-1-to-amazon-nova-2-on-amazon-bedrock/)

The worksheet applies those sources to this book's example. It is the author's
proposed review record, not a claim that AWS mandates this exact template.
