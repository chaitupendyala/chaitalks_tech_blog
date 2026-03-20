---
title: "Busy Beavers: Part 3: How Far We've Come – and How Far We Can't Go (Yet)"
date: 2025-05-12
categories: 
  - "computer-science"
  - "mathematics"
tags: 
  - "alan-turing"
  - "algorithms"
  - "foundational-computer-science"
  - "limits-of-computation"
  - "mathematical-puzzles"
  - "number-theory-potential-connection-due-to-rapid-growth"
  - "open-problems-in-computer-science-2"
  - "state-machine"
  - "theory-of-computation"
series: "Busy Beavers Series"
---

In [Part 1](https://chaitalks.tech/posts/busy-beavers-part-1-what-is-a-turing-machine/) and [Part 2](https://chaitalks.tech/posts/busy-beavers-part-2-diving-deeper/) of this series, we set up the question: given a Turing machine with n states running on a blank tape, what's the maximum number of steps it can take before halting? We saw how that clean, finite-sounding question leads directly into undecidability, incompleteness, and the outer edge of what's knowable.

Now let's look at where things actually stand.

* * *

## What We Actually Know

The challenge with the Busy Beaver problem is that for small n, it's hard. For large n, it's provably impossible. But "small" here is relative. Researchers have put enormous effort into confirming values for the first five cases.

Here's what's been proven:

- **n = 1**: S(1) = 1, Σ(1) = 1
- **n = 2**: S(2) = 6, Σ(2) = 4
- **n = 3**: S(3) = 21, Σ(3) = 6
- **n = 4**: S(4) = 107, Σ(4) = 13
- **n = 5**: S(5) = 47,176,870, Σ(5) = 4,098

Notice the jump from n = 4 to n = 5. 107 steps becomes nearly 47 million. These weren't guesses. Each value required exhaustive enumeration of candidate machines, clever pruning to cut down the search space, and rigorous mathematical proofs that nothing was missed.

* * *

## n = 6 and Beyond

At n = 6, things change in kind, not just in degree.

One known 6-state machine runs for over **7.4 × 10¹⁹ steps** before halting, assuming it ever does. We think it halts, but we can't yet prove it. Entire papers have been devoted to analysing what that machine does, phases that simulate counters, nested loops, fragments of other computations. It's bizarre to stare at.

At n = 7 or n = 8, there are candidate machines where no one even has a confident guess about whether they halt. Their behavior is intricate enough that they're genuinely hard to distinguish from machines that run forever.

* * *

## Where Logic Itself Runs Out

This is the part I find most interesting. The Busy Beaver problem isn't just computationally hard, it's provably uncomputable. No algorithm can calculate Σ(n) for all n. That's not a gap in our current knowledge that better computers might fix, it's a permanent limitation in what algorithms can do.

It goes deeper than that. Some Busy Beaver values may require logic **stronger than ZFC**, the standard axiomatic foundation that essentially all of modern mathematics is built on, to prove. Not stronger computers. Stronger axioms. We might be dealing with numbers that are perfectly well-defined and true, but that sit outside the reach of any proof system we currently have.

That's an uncomfortable thing to accept. There are specific integers whose values we can never know.

* * *

## Could AI Help?

Maybe, at the margins. AI systems are already being used to classify machine behavior and assist with proof search. But the fundamental barrier here isn't about intelligence or compute power, it's about what's provable. No matter how capable an AI becomes, it can't resolve questions that are undecidable. It would hit the same wall.

What AI might do is help us push slightly further, find better proofs for cases near the boundary, classify more machines faster. But the horizon itself doesn't move.

* * *

## Final Thoughts

The Busy Beaver problem starts as a cute puzzle: which machine writes the most 1s? But follow it far enough and it becomes a very direct confrontation with the limits of formal reasoning.

We've confirmed values up to n = 5 through heroic effort. Beyond that, we're increasingly in territory where the tools of mathematics stop working, not because we lack the skill to apply them, but because the questions themselves escape what any consistent formal system can answer.

I find that genuinely humbling. Not in a discouraging way, but in the way that reminds you how strange and vast the space of ideas really is. Some peaks are too high to climb, not from lack of effort, but because the summit is beyond the horizon of logic itself.
