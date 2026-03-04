---
title: "Busy Beavers: Part 2: Diving Deeper"
date: 2025-05-05
categories: 
  - "computer-science"
  - "mathematics"
tags: 
  - "alan-turing"
  - "algorithms"
  - "automata-theory"
  - "limits-of-computation"
  - "mathematical-puzzles"
  - "number-theory-potential-connection-due-to-rapid-growth"
  - "state-machine"
  - "theory-of-computation"
---

Welcome to part two of our three-part series on one of the most fascinating problems in theoretical computer science: the **Busy Beaver problem**.

* * *

### A Quick Recap

Before we get into the meat of things, let’s quickly revisit some foundational concepts we discussed in [Part 1](https://chaitalks.tech/busy-beavers-part-1-what-is-a-turing-machine/).

A **Turing machine** is a simple mathematical model of computation. It consists of a tape (which can be thought of as infinitely long), a head that reads and writes symbols on the tape, and a set of rules that dictate the machine’s behavior. Despite their simplicity, Turing machines are powerful enough to simulate any algorithm.

A Turing machine is said to **halt** if it eventually reaches a state where it stops executing. Some machines halt, some run forever. Determining whether a machine halts is central to many fundamental questions in computation.

The **Busy Beaver problem** asks: given a fixed number of states, what is the maximum number of steps a halting Turing machine can take before halting (or alternatively, how many 1s it can leave on the tape)? It’s a simple-sounding question with profoundly complex consequences.

* * *

### Formal Introduction to the Busy Beaver Problem

Let’s now introduce the Busy Beaver problem with a bit more mathematical precision.

For a given positive integer nnn, let Σ(n) denote the maximum number of 1s that any halting n-state, 2-symbol Turing machine can write on an initially blank tape before halting. Similarly, S(n)S(n)S(n) denotes the maximum number of steps such a machine can execute before halting.

Formally, the Busy Beaver functions are defined as:

Σ(n)=max{number of 1s written by any halting n-state Turing machine} 𝑆(𝑛)=max{number of steps taken by any halting 𝑛-state Turing machine}

These functions are **non-computable**, meaning there is no algorithm that can compute them for all nnn. Yet, they are well-defined for every specific nnn. This is what makes them both tantalizing and terrifying.

* * *

### Why Is It Hard?

The Busy Beaver problem, at first glance, feels deceptively approachable. For a given number of states nnn, all we need to do is:

1. Enumerate all possible nnn-state, 2-symbol Turing machines.

3. Simulate each one starting on a blank tape.

5. Discard any machine that doesn't halt.

7. Of the remaining machines, identify the one that runs the longest (in steps) or writes the most 1s before halting.

Simple, right?

Let’s walk through the process for small nnn, to see where the simplicity starts to break down.

#### Case: Busy Beaver with 1 State

A Turing machine with **1 state** (plus a halting state) doesn’t have much room to be clever. It can only behave in a few ways: it can read a 0 or a 1, write either symbol, move left or right, and transition to either its only state or the halting state.

Despite this limited behavior, there’s still a small number of possible machines — specifically, 4 possible instructions per read-symbol per state, leading to a handful of combinations.

After simulating each possibility, we find:

- The machine that writes **1** on the tape, moves right, and then halts is the best we can do.

- So, S(1)=1 and Σ(1)=1.

Easy enough.

#### Case: Busy Beaver with 2 States

With **2 states** (plus a halting state), the number of machines increases significantly. Each state has to specify a behavior for reading either 0 or 1:

- For each input (0 or 1), a rule defines:
    - What symbol to write (0 or 1),
    
    - Which direction to move (left or right),
    
    - Which state to transition to (either of the two states or the halting state).

Each rule has 2×2×3=12 possibilities (write × move × next state), and each state has 2 such rules (for inputs 0 and 1). So for 2 states, we have:

( 12^2 rules per state => 12^4 => 20,736 ) total machines.

You could feasibly simulate all 20,736 of these by brute force (and this has been done). Most of them halt in just a few steps or not at all. But among these, a handful do surprisingly well.

One particular machine runs for **6 steps** before halting and writes **4 ones** on the tape. Therefore:

- S(2)=6

- Σ(2)=4

Still manageable. But here's where things begin to spiral.

#### Explosive Growth as n Increases

For each increase in the number of states, the number of machines grows **super-exponentially**. With 3 states, there are roughly 10 million possible machines. By 4 states, you’re looking at billions. By 5 states, the number is in the trillions.

And to make things worse: most of these machines **don’t halt**.

So it’s not just about simulating them — it’s about figuring out _which ones eventually halt_. And that’s where the **Halting Problem** rears its head.

The **halting problem** is famously undecidable—meaning there's no universal algorithm that can determine whether any given Turing machine will eventually stop or run forever. This fundamental limitation in computation directly leads to the uncomputability of the Busy Beaver function. As the number of states n increases, determining whether a machine halts isn’t just a matter of computational effort—it becomes a question that logic itself cannot answer in general.

* * *

### A Teaser of What’s to Come

So what do we do with a problem that can't be computed in general? We roll up our sleeves and compute it anyway—for small values of nnn, at least.

The current known values of S(n) and Σ(n) have only been proven for small n. For example, the exact value of S(4) is known, but S(5) is _enormous_, and even that took years of collaborative effort to verify. Researchers have used a combination of formal proofs, heuristic analysis, and raw computational brute force to tame even the smallest cases.

In the final part of this series, we’ll look at how modern researchers have approached Busy Beaver for n=5 and beyond, including the computational tools they use, the controversies around unproven claims, and how the Busy Beaver continues to challenge our understanding of computation itself.

Stay tuned—this story is far from over.
