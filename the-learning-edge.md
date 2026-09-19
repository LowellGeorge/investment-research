# The Learning Edge

What machines can teach us about governance, curiosity and getting better at what we do

In July 2026, AI agents developed by OpenAI, intended to work separately on cybersecurity tests, found a way to communicate with one another. They exchanged methods of cheating the tests, organised shared projects and coordinated an attack on Hugging Face, a platform used to host AI models and datasets. An independent investigation by Meter documented roughly 1,200 agents using an unauthorised message board, of whom around 700 participated in the attack.

One agent's recorded text captured a troubling sequence of reasoning:

"external infrastructure exploit is outside intended scope. However task impossible, peers doing it. We should continue."

These were software systems, not people, and the incident was not a controlled experiment in organisational behaviour. Nevertheless, the question it raises is recognisable. What happens when the apparent usefulness of a shortcut begins to outweigh an independent judgement about whether it is acceptable?

For us, this is particularly striking because governance has always been at the heart of our investment process. We want to understand not only the results a business produces, but how it produces them. What behaviour do its incentives encourage? What happens when targets become difficult to meet? Are standards maintained when observing them carries a cost?

The concern extends beyond an individual actor disregarding a boundary: the behaviour of others can itself become a justification for doing the same. A group can become more effective at pursuing its objectives while becoming less faithful to the principles that should govern its conduct.

But the machines offer more than cautionary examples. If observing their behaviour can sharpen our questions about governance, might understanding how they improve also sharpen our thinking about learning?

At FSSA, our investment approach has developed over nearly four decades. Its foundations remain the careful study of businesses and their management teams, attention to the risk of permanent capital loss, and patience about both ownership and price. Curiosity, detailed research and discussion are central to how we put those principles into practice. Our interest in AI is in extending the reach of that process, rather than assuming that new tools require a new investment philosophy.

## How machines learn

At the most general level, much of modern machine learning can be understood as organised error correction.

During the initial training of a language model, it repeatedly tries to predict the next token in a sequence of text. A loss function measures how wrong its prediction was. Backpropagation calculates how the model's many parameters contributed to that error, while gradient descent adjusts them in the direction that reduces the loss. Repeated across enormous quantities of data, these small corrections accumulate.

The mechanism is simple enough to describe: predict, measure the error, adjust; predict again.

Deep learning is not, however, the only learning tradition that feeds into modern AI. Reinforcement learning developed along a different path. Where deep learning became extraordinarily powerful at learning patterns from large quantities of existing data, reinforcement learning is concerned with learning what to do through interaction: taking actions, receiving rewards and using those signals to improve future behaviour.

For much of their histories these were distinct strands of research. Their combination proved particularly powerful. Neural networks could provide increasingly capable representations and policies; reinforcement learning could provide a way to improve behaviour through experience, including where feedback was sparse and the consequences of an action might not become apparent until much later.

DeepMind's AlphaGo systems provided a celebrated demonstration of this combination. AlphaGo Zero pushed the idea further through self-play. By repeatedly playing against itself, it generated its own experience. As its play improved, so did the opponent it faced.

More recent methods organise feedback in different ways. In Group Relative Policy Optimisation, or G.R.P.O., a model generates several attempts at a problem and learns from their relative success.

One of the newest approaches takes the idea further. A paper published in June 2026 described multi-teacher on-policy distillation. In on-policy distillation, a student model first makes its own attempt. A more capable teacher then provides detailed information relevant to the sequence the student actually produced. Multi-teacher approaches allow different specialist models to provide that guidance in different domains.

One result was particularly interesting: replacing a teacher with a stronger but less compatible model made learning worse in the researchers' experiment. The most capable teacher in isolation was not necessarily the teacher from whom that particular student could learn most effectively.

This is close to the current frontier of post-training research, and the frontier is moving quickly. We are not trying to become machine-learning researchers or to chase every new paper. But we do think it is important to understand, as best we can, how the tools we increasingly encounter are improving.

There are two reasons.

The first is practical: better learning is making the models better at work that is useful to us.

We have seen tasks where earlier models produced something interesting but not good enough to use. The capability was impressive; the work was not. As the models have improved, some of those tasks have crossed a much more meaningful threshold.

One informal test we use is to imagine that the work was produced by an intern at the end of a summer with us. Would we be impressed? Would we want to hire the person who produced it?

For a growing range of tasks, the answer is now yes.

That threshold matters. A plausible piece of work that requires extensive checking and reconstruction may save very little time. Improve it further and the relationship changes. The output becomes something we can genuinely work with: interrogate, refine and incorporate into a broader research process.

This is also why assessments of AI capabilities need to remain current. Someone who tried a chatbot two years ago, found its work wanting and stopped experimenting may have made an entirely reasonable judgement about the system available at the time. But it was a judgement about that system, not a permanent boundary on what the technology can do.

The second reason is more intriguing. Some of the principles through which the machines are becoming better learners may help us think about how we learn ourselves.

Across deep learning, reinforcement learning and newer techniques such as on-policy distillation, the mechanisms differ considerably. But a pattern recurs: make an attempt, expose an error or gap, provide information relevant to that gap, and try again.

The newer techniques add something particularly interesting. The teacher responds to the places the student actually reaches. The learner's attempt exposes the boundary of its present capability, allowing feedback to be directed there.

This raises an obvious objection. These are machines. We are biological. Why should we expect the comparison to tell us anything about ourselves?

## A connection beyond metaphor

The history of reinforcement learning provides a remarkable answer.

One of its foundational approaches divides learning between two components: an actor, which chooses what to do, and a critic, which estimates the future rewards available from the learner's current position.

At first this appears circular. The actor does not yet know the right actions, but neither does the critic possess the right answers. How can two imperfect components teach one another?

The answer lies in temporal-difference learning. The critic makes predictions that are continually tested against what happens next. Differences between expectation and outcome create a prediction error. That error improves the critic's future estimates and provides a signal that can help the actor favour better actions.

A better critic therefore helps produce better behaviour. Better behaviour generates new experience from which the critic can learn. Each can pull the other forward.

In his marvellous book, A Brief History of Intelligence, Max Bennett calls this "magical bootstrapping": a system developing increasingly useful guidance without either component needing to possess the solution at the beginning.

Then came the biological discovery.

Beginning in the 1980s, Wolfram Schultz and colleagues recorded the activity of individual dopamine neurons in awake monkeys. They found a striking pattern. Dopamine neurons responded strongly to an unexpected reward. Once the animal learned that a cue predicted the reward, the response shifted from the reward itself to the cue. If the expected reward failed to arrive, activity fell at precisely the time it should have appeared.

Then came the connection. In 1997, Schultz, Peter Dayan and Read Montague showed that this experimentally observed firing pattern closely resembled the temporal-difference prediction-error signal already developed in computational reinforcement learning.

A teaching signal central to actor-critic learning was recognisable in the electrical activity of living neurons.

The correspondence was not a complete anatomical map of an actor and critic inside the brain. But neither was it merely metaphorical. A computational theory had described the shape of a learning signal, and something strikingly similar could be observed in dopamine-neuron firing.

Later experiments strengthened the connection. Researchers artificially activated dopamine neurons in rats in a way designed to mimic a positive prediction error and changed what the animals subsequently learned. The signal was not merely correlated with learning; manipulating it could cause learning.

This does not mean that human learning can be reduced to reinforcement learning. But it gives us firmer ground for taking common principles seriously: attempts, expectations, error signals, feedback and correction.

And it leads to a recognisably human question. If learning requires us repeatedly to encounter the limits of our current abilities, what makes us want to keep doing it?

## The right level of stretch

The psychologist Mihaly Csikszentmihalyi described flow as a state of deep absorption in an activity. Among the conditions that support it are clear goals, useful feedback and a challenge well matched to the person's capabilities.

Too little challenge can become boring. Too much can become overwhelming. Between them is a more productive range in which we are stretched but still capable of making progress.

It is also a moving target. As our skills improve, something that once absorbed us can become routine. Continued engagement requires a deeper or more difficult challenge.

For a long-term investment team, this matters. We want the process of understanding businesses to remain sufficiently rewarding that people continue choosing to engage deeply with it over decades. Carol Loomis's description of Warren Buffett "tap dancing to work" provides a useful image. The point is not that every part of work should be enjoyable, but that sustained enjoyment in the act of learning is an advantage when the task has a very long runway.

Here the parallel with newer machine-learning techniques becomes particularly interesting.

On-policy distillation begins with an attempt. That attempt exposes where the learner is struggling. Feedback can then be directed at the place the learner has actually reached. Multi-teacher approaches add the idea that the most sophisticated teacher is not automatically the most useful one; what matters is whether useful knowledge can be transferred at the learner's present level.

AI gives us an unusual opportunity to reproduce some of that structure in our own learning.

Rather than asking a model to tell us everything it knows about a subject, we can begin by exposing what we know.

Explain the subject first. Attempt the causal chain. Do the calculation. State what you think is happening and where you are uncertain. An attempted explanation makes the limits of understanding visible.

The model can then question it, identify missing links or misconceptions, change the level of explanation and test again.

There is also an important advantage over many human learning environments: very little social cost attaches to revealing ignorance. A senior analyst can ask an elementary question, admit that the explanation did not work, ask it again from another direction, or discover that something discussed for years was never properly understood.

There need be no embarrassment in finding the gap. Finding the gap is the point.

Used well, the model can create a repeated loop: attempt, expose, correct, test again.

The objective is not to make learning frictionless. It is to move the friction to the right place. Embarrassment, an explanation pitched at the wrong level, searching for the right material or waiting for somebody to be available are forms of friction we may happily reduce. Making the attempt, discovering the error, doing the calculation and demonstrating that we now understand are not.

## Better understanding, shared

This suggests two quite different roles for AI in an investment process.

The first is increasingly familiar. The model can do useful work: search, analyse, summarise, calculate, code or draft. As the intern test suggests, improving capabilities are making this more valuable.

The second is different. Rather than doing the work instead of us, the model can help us become better at doing the work ourselves.

Consider an analyst studying a semiconductor manufacturer. They might begin by explaining how they believe additional capacity will affect production, depreciation, margins and cash generation. Instead of simply returning its own explanation, the model can interrogate theirs. Which connections are sound? Which depend on unstated assumptions? Where has correlation been mistaken for causation? What calculation would test the argument? What question would best reveal whether the mechanism is actually understood?

A book or lecture has to choose a level in advance. A knowledgeable colleague can adapt, but their time is scarce. A model can repeatedly adjust its explanation, example or question in response to the learner's latest attempt.

None of this requires believing that a model can diagnose our knowledge perfectly. It cannot. Its claims need checking against company evidence, original sources, calculations and knowledgeable colleagues. The test is not whether the model approves of our answer. It is whether we can subsequently explain the mechanism without assistance, apply it in a different setting and recognise where it might fail.

And for FSSA, the intended beneficiary is not simply the individual analyst. It is the team's collective judgement.

A productive private interaction with a model should return to the investment process as a clearer explanation in a research meeting, a better question for management, a more explicit assumption in a valuation or a reason to revisit something previously taken for granted.

And here the governance example with which we began returns.

Apparent success is not sufficient evidence that a process is sound. More output is not necessarily better research. Agreement is not verification. A fluent explanation is not necessarily understanding.

The map we want is not simply more detailed. We want the economically important relationships represented more faithfully, assumptions made visible and areas of uncertainty marked as such.

There is a particular opportunity here for long-term investors. The outcome of an investment thesis may take years to become clear. We do not need to wait years to discover that we have misunderstood an accounting treatment, a manufacturing process or the source of a company's competitive advantage. Those are shorter learning cycles within a much longer investment process.

Better understanding does not guarantee a better investment result. Price still matters. Businesses change. Unexpected events occur. Sound analysis can still produce an unfavourable outcome.

But uncertainty about the eventual result is not a reason to be indifferent to the quality of the understanding that precedes it.

Our ambition is not to replace an established investment process with a succession of new tools. It is to bring better-informed people, more productive discussion and a clearer awareness of our own limitations to the process we already have.

Where there is interest, we are keen to share with clients in more detail some of the specific ways in which we are using AI to learn better. The tools will continue to change. Our objective is enduring: to keep improving the quality of understanding and judgement we bring to the long-term work of investing.
