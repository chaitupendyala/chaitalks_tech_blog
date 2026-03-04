---
title: "Busy Beavers: Part 1 — What is a Turing Machine?"
date: 2025-04-28
categories: 
  - "computer-science"
  - "mathematics"
tags: 
  - "alan-turing"
  - "algorithms"
  - "automata-theory"
  - "bbn"
  - "busy-beaver"
  - "computability"
  - "computational-complexity"
  - "computer-science"
  - "foundational-computer-science"
  - "halt-state"
  - "halting-problem"
  - "infinite-tape"
  - "limits-of-computation"
  - "mathematical-puzzles"
  - "mathematics"
  - "non-computable"
  - "number-theory-potential-connection-due-to-rapid-growth"
  - "open-problems-in-computer-science-2"
  - "recreational-mathematics"
  - "sn"
  - "state-machine"
  - "theoretical-computer-science"
  - "theory-of-computation"
  - "tibor-rado"
  - "turing-machine"
coverImage: "image.png"
---

Welcome to the first post in my three-part series exploring one of the most fascinating topics in all of mathematics and computer science: the **Busy Beaver Problem**.

Before diving into the chaos and wonder of Busy Beavers, I want to start with the surprisingly simple idea that makes it all possible: the **Turing Machine**.

* * *

## Imagine the Simplest Robot You Can

Picture a tiny robot crawling along an endless strip of paper.

This little machine can:

- Look at the square it's standing on.

- Write a mark (`0` or `1`) on that square.

- Move one step left or right.

- Change its internal "mood" or **state**.

No memory. No cleverness. Just following a strict set of instructions.

That’s the heart of a **Turing Machine**, invented by [Alan Turing](https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf) back in 1936.

_(Believe it or not, every laptop, phone, and server today is just an extremely complicated Turing Machine!)_

* * *

## What Actually Makes a Turing Machine?

A Turing Machine is built from just a few simple parts:

- **A tape**: An infinite row of squares, each holding a symbol (`0` or `1`).

- **A head**: A device that reads and writes symbols on the tape.

- **A finite set of states**: Think of them like the robot's moods.

- **Transition rules**: Instructions like: "If you're in state A and you see a `0`, write a `1`, move right, and switch to state B."

At each step, the machine:

1. Reads the symbol underneath it.

3. Writes a new symbol (or overwrites the current one).

5. Moves left or right by one square.

7. Switches to a new state — or halts.

* * *

## When Does a Turing Machine Halt?

Sometimes, a Turing Machine gets to a point where no instructions tell it what to do next.  
When that happens, it **halts** — the machine freezes, stops writing, and stops moving.

Halting matters because it marks the end of a computation.  
In fact, Alan Turing proved in his famous [Halting Problem](https://en.wikipedia.org/wiki/Halting_problem) that **there’s no universal way to tell whether a machine will halt or run forever**.

* * *

## A Tiny Turing Machine in Action (With Two States)

Let me show you a slightly more interesting Turing Machine:

<figure>

| Current State | Read Symbol | Write Symbol | Move | Next State |
| --- | --- | --- | --- | --- |
| A | 0 | 1 | R | B |
| B | 0 | 1 | R | HALT |

<figcaption>

Two State Turing Machine

</figcaption>

</figure>

![](images/Turing_machine.drawio.png)

Here's how it plays out:

1. The machine starts in **state A**, sitting over a blank cell (`0`).

3. It writes a `1`.

5. It moves one square to the right.

7. It switches to **state B**.

9. In **state B**, it again finds a blank (`0`).

11. It writes a `1`.

13. It moves one square to the right.

15. Now there are no rules left — the machine **halts**.

**Result:** Two `1`s are written next to each other on the tape before stopping.

#### Quick Visual of the Tape Evolution

```
Initial Tape: [ 0 ][ 0 ][ 0 ]...

Step 1: (State A)
- Write 1
- Move right
- Switch to State B

Tape: [ 1 ][ 0 ][ 0 ]...

Step 2: (State B)
- Write 1
- Move right
- Halt

Final Tape: [ 1 ][ 1 ][ 0 ]...
```

* * *

## What Does "Size" Mean for a Turing Machine?

Before getting into Busy Beavers, there's one important idea to understand:

When I talk about the "**size**" of a Turing Machine, I mean **how many states** it has (excluding the halting state).

For example:

- The simple machine above had **two states**: A and B.

- A machine with **three states** might have states A, B, and C, and so on.

The more states you allow, the more complicated a machine can become.  
More states mean more possibilities — and even a slight increase can lead to mind-boggling complexity.

* * *

## The First Glimpse of the Busy Beaver

Now, imagine:

> **Among all possible Turing Machines with a given number of states, which one writes the most 1s before halting?**

This innocent-sounding question leads straight to the [Busy Beaver Problem](https://en.wikipedia.org/wiki/Busy_beaver), introduced by mathematician [Tibor Radó](https://link.springer.com/article/10.1007/BF01386390) in 1962.

And here's the catch:

- Even with just 4 or 5 states, finding the "busiest" machine becomes ridiculously difficult.

- The number of steps or 1s can explode faster than any computable function.

- The Busy Beaver function eventually grows faster than anything a computer could possibly calculate.

Simple machines. Infinite complexity.

* * *

## What’s Coming Next

This is just **Part 1** of my three-part series.

In **Part 2**, I’ll dive headfirst into the Busy Beaver Problem itself:

- How it’s formally defined.

- Why tiny machines can produce massive outputs.

- A few legendary Busy Beaver examples that will blow your mind.

It’s only going to get wilder from here.
