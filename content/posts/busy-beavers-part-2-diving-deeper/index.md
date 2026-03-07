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

Welcome to part two of my three-part series on the **Busy Beaver problem**.

* * *

### A Quick Recap

If you haven't read [Part 1](https://chaitalks.tech/posts/busy-beavers-part-1-what-is-a-turing-machine/) yet, here's the short version.

A **Turing machine** is a minimal model of computation: an infinite tape, a read/write head, a set of states, and a set of rules. Despite how simple that sounds, Turing machines are powerful enough to simulate any algorithm. A machine is said to **halt** if it eventually reaches a state where it stops executing. Some machines halt, some run forever, and here's the uncomfortable part: in general, you can't tell which is which without just watching.

The **Busy Beaver problem** asks: for a given number of states, what's the maximum number of steps a halting Turing machine can take before stopping? Or equivalently, how many 1s can it leave on an initially blank tape? It's a simple question with consequences that are genuinely hard to wrap your head around.

* * *

### The Formal Setup

Let's be a bit more precise. For a positive integer n, define:

- **Σ(n)**: the maximum number of 1s that any halting n-state, 2-symbol Turing machine can write on a blank tape before halting.
- **S(n)**: the maximum number of steps such a machine can execute before halting.

These functions are **non-computable**. There is no algorithm that calculates them for all n. They grow faster than any function a computer can produce. And yet, for any specific n, they have exact values that are simply true. You just might not be able to prove what those values are.

That tension, well-defined but unknowable, is at the heart of why this problem is so strange.

* * *

### Why Is It Hard?

At first glance the approach looks straightforward enough. For a given n:

1. Enumerate all possible n-state, 2-symbol Turing machines.
2. Simulate each one from a blank tape.
3. Throw out any that don't halt.
4. Of the ones that do halt, find the one that ran longest or wrote the most 1s.

Let's see how that holds up for small n.

#### 1 State

A 1-state machine doesn't have much room to work with. After accounting for all combinations, the best it can do is write a single 1 and halt. So S(1) = 1 and Σ(1) = 1. Easy.

#### 2 States

With 2 states, the number of possible machines jumps significantly. Each state needs a rule for reading a 0 and a rule for reading a 1. Each rule specifies what to write, which direction to move, and which state to go to next. Work it out and you get 20,736 possible 2-state machines. That's still feasible to brute-force, and researchers have done exactly that.

The winner runs for **6 steps** and writes **4 ones** before halting. So S(2) = 6 and Σ(2) = 4. Still manageable.

#### Then It Blows Up

For 3 states, you're looking at around 10 million possible machines. For 4 states, billions. For 5 states, trillions. And most of them don't halt.

So the challenge isn't just running the simulations. It's figuring out which machines actually halt, and that's where the **Halting Problem** becomes the obstacle. Turing proved there's no general algorithm for deciding whether an arbitrary Turing machine halts. That undecidability doesn't just slow things down, it makes the Busy Beaver function fundamentally uncomputable. As n grows, no amount of cleverness or compute can get you there in general. You hit a wall that's not about processing power, it's about what logic itself can answer.

* * *

### What Comes Next

So what do you do with a problem that can't be solved in general? You solve it anyway, for small cases, by rolling up your sleeves and combining brute force with mathematical ingenuity.

The values of S(n) and Σ(n) have only been confirmed for small n. S(5) is known now, but it took years of collaborative work across researchers, formal proofs, and raw computation to nail it down. And even that pales compared to what happens at n = 6.

In Part 3, we'll look at what's been confirmed, what's still unresolved, and just how quickly this problem escapes everything we know how to do.
